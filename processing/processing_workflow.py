import os
import logging
from typing import List
from pdf_extraction.extract_text import extract_text
from pdf_extraction.extract_invoice_data import extract_invoice_data
from pdf_extraction.extract_site_totals import extract_site_totals
from database.database_utils import get_db_connection, insert_site_data, insert_invoice_site_totals, truncate_sites_table, fetch_data
from utils.logger import setup_logger
from decimal import Decimal

setup_logger()
logger = logging.getLogger(__name__)


def process_pdf(pdf_path: str, socketio=None) -> None:
    """Processes a single PDF file, extracts data, and saves it to the database.

    Args:
        pdf_path (str): The path to the PDF file.
        socketio: SocketIO instance for real-time updates (optional).
    """
    try:
        logger.info(f"Processing PDF: {pdf_path}")
        if socketio:
            socketio.emit('processing_update', {'filename': os.path.basename(
                pdf_path), 'status': 'Extracting text'})

        pdf_text = extract_text(pdf_path)
        # print("Extracted PDF Text:\n", pdf_text)
        if not pdf_text:
            raise ValueError(f"Could not extract text from {pdf_path}")

        logger.debug(f"Extracted PDF text: {pdf_text}")

        if socketio:
            socketio.emit('processing_update', {'filename': os.path.basename(
                pdf_path), 'status': 'Extracting invoice data'})
        invoice_data = extract_invoice_data(pdf_text)
        logger.info(f"Extracted invoice data: {invoice_data}")

        # Validate invoice_data
        required_fields = ['invoice_id', 'payment_date',
                           'transaction_id', 'total_amount', 'batch_id']
        for field in required_fields:
            if field not in invoice_data or invoice_data[field] is None:
                logger.warning(f"Skipping PDF due to missing field: {field}")
                return

        if socketio:
            socketio.emit('processing_update', {'filename': os.path.basename(
                pdf_path), 'status': 'Extracting site totals'})
        site_names = _get_site_names_from_db()
        site_totals = extract_site_totals(
            pdf_text, site_names)
        logger.info(f"Extracted site totals: {site_totals}")

        if socketio:
            socketio.emit('processing_update', {'filename': os.path.basename(
                pdf_path), 'status': 'Saving to database'})

        conn = get_db_connection()
        with conn:
            invoice_id = insert_invoice(conn, invoice_data)
            _insert_invoice_site_totals(conn, invoice_id, site_totals)

        if socketio:
            socketio.emit('processing_update', {
                          'filename': os.path.basename(pdf_path), 'status': 'Completed'})
        logger.info(f"PDF processed successfully: {pdf_path}")

    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {e}", exc_info=True)
        if socketio:
            socketio.emit('processing_update', {'filename': os.path.basename(
                pdf_path), 'status': f'Error: {str(e)}'})


def insert_invoice(conn, invoice_data: dict) -> str:
    """Inserts data into the invoices table and returns the invoice_id."""

    try:
        # Validate invoice_data
        required_fields = ['invoice_id', 'payment_date',
                           'transaction_id', 'total_amount', 'batch_id']
        for field in required_fields:
            if field not in invoice_data or invoice_data[field] is None:
                logger.error(f"Missing or null field in invoice_data: {field}")
                raise ValueError(f"Missing or null field: {field}")

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoices (
                    invoice_id, payment_date, transaction_id, total_amount, batch_id
                ) VALUES (%s, %s, %s, %s, %s)
                RETURNING invoice_id
                """,
                (
                    invoice_data.get('invoice_id'),
                    invoice_data.get('payment_date'),
                    invoice_data.get('transaction_id'),
                    invoice_data.get('total_amount'),
                    invoice_data.get('batch_id'),
                ),
            )
            invoice_id = cur.fetchone()[0]
            return invoice_id
    except Exception as e:
        logger.error(
            f"Error inserting into invoices table: {e}", exc_info=True)
        raise


def _insert_invoice_site_totals(conn, invoice_id: str, site_totals: dict) -> None:
    """Helper function to insert site total data into the database."""

    try:
        with conn.cursor() as cur:
            for site_name, site_total in site_totals.items():
                cur.execute(
                    """
                    INSERT INTO invoice_site_totals (
                        invoice_id, site_name, site_total
                    ) VALUES (%s, %s, %s)
                    """,
                    (
                        invoice_id,
                        site_name,
                        site_total,
                    ),
                )
    except Exception as e:
        logger.error(
            f"Error inserting invoice site totals: {e}", exc_info=True)
        raise


def process_all_pdfs(upload_folder: str, socketio=None) -> None:
    """Processes all PDF files in the given upload folder.

    Args:
        upload_folder (str): The path to the folder containing PDF files.
        socketio: SocketIO instance for real-time updates (optional).
    """
    pdf_files = [f for f in os.listdir(
        upload_folder) if f.lower().endswith('.pdf')]
    total_files = len(pdf_files)
    logger.info(f"Found {total_files} PDF files in {upload_folder}")

    for i, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(upload_folder, pdf_file)
        logger.info(f"Processing file {i + 1}/{total_files}: {pdf_path}")
        if socketio:
            socketio.emit('batch_processing_update', {
                          'current': i + 1, 'total': total_files, 'filename': pdf_file, 'status': 'Processing'})
        process_pdf(pdf_path, socketio)

    logger.info("All PDFs processed.")
    if socketio:
        socketio.emit('batch_processing_complete', {
                      'message': 'All files processed'})


def _get_site_names_from_db() -> List[str]:
    """Helper function to fetch site names from the database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM sites")
            site_names = [row[0] for row in cur.fetchall()]
        return site_names
    except Exception as e:
        logger.error(
            f"Error fetching site names from database: {e}", exc_info=True)
        return []
    finally:
        if conn:
            conn.close()


def _insert_site_data(conn, site_names: List[str]) -> dict:
    """Helper function to insert site names into the database and get their IDs."""
    site_ids = {}
    try:
        with conn.cursor() as cur:
            for name in site_names:
                cur.execute(
                    "INSERT INTO sites (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
                    (name,),
                )
                result = cur.fetchone()
                if result:
                    site_ids[name] = result[0]
                else:
                    # Fetch the ID if it already exists
                    cur.execute(
                        "SELECT id FROM sites WHERE name = %s", (name,))
                    site_ids[name] = cur.fetchone()[0]
        return site_ids
    except Exception as e:
        logger.error(f"Error inserting site data: {e}", exc_info=True)
        raise
