import os
import sys
import json
import logging
import psycopg2
from config import DATABASE_URL
from psycopg2 import sql
# from utils.json_parser import parse_json_data

logging.basicConfig(level=logging.DEBUG)


def save_grand_totals_to_db(grand_totals, batch_id):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                for site_name, total in grand_totals['grand_totals'].items():
                    query = """
                        INSERT INTO grand_totals (batch_id, site_name, total, total_of_grand_totals)
                        VALUES (%s, %s, %s, %s);
                    """
                    values = (batch_id, site_name, total,
                              grand_totals['total_of_grand_totals'])
                    cur.execute(query, values)
                conn.commit()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise


def save_invoice_to_db(invoice_data, batch_id, filename):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Assuming invoice_data is a dictionary
                query = """
                    INSERT INTO invoices (batch_id, filename, payment_date, transaction_id, total)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """
                values = (batch_id, filename, invoice_data.get('payment_date'), invoice_data.get(
                    # Get data from invoice_data
                    'transaction_id'), invoice_data.get('total'))
                cur.execute(query, values)
                invoice_id = cur.fetchone()[0]  # Get the returned invoice ID
                conn.commit()
                return invoice_id  # Return the ID
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise  # Re-raise the exception


def fetch_invoice_data_from_db(batch_id):
    logging.debug(f"Fetching invoice data for batch_id: {batch_id}")

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Fetch invoice details along with grand totals for the given batch_id
                query = """
                    SELECT
                        i.filename,
                        i.payment_date,
                        i.transaction_id,
                        i.total AS invoice_total,
                        gt.site_name,
                        gt.total AS site_total,
                        gt.total_of_grand_totals
                    FROM
                        invoices i
                    LEFT JOIN
                        grand_totals gt ON i.batch_id = gt.batch_id
                    WHERE
                        i.batch_id = %s;
                """
                logging.debug(f"Executing SQL Query: {query}")
                cur.execute(query, (batch_id,))
                results = cur.fetchall()
                logging.debug(f"Query Results: {results}")

                # Format the results into a list of dictionaries
                formatted_results = []
                for row in results:
                    formatted_results.append({
                        'filename': row[0],
                        'payment_date': row[1],
                        'transaction_id': row[2],
                        'invoice_total': row[3],
                        'site_name': row[4],
                        'site_total': row[5],
                        'total_of_grand_totals': row[6]
                    })
                return formatted_results
    except psycopg2.Error as e:
        print(f"Database error: {e}")


def populate_invoice_to_db(connection, cursor, invoice_data):
    """Inserts invoice data into the database."""
    try:
        query = sql.SQL(
            """
            INSERT INTO invoices (transaction_id, batch_id, details)
            VALUES (%s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING;
            """
        )
        cursor.execute(query, (
            invoice_data["transaction_id"],
            invoice_data["batch_id"],
            json.dumps(invoice_data["details"]),
        ))
        connection.commit()
        logging.info(f"Inserted invoice: {invoice_data['transaction_id']}")
    except Exception as e:
        logging.error(
            f"Error inserting invoice {invoice_data['transaction_id']}: {str(e)}")
        raise

# def process_file(file_path):
    """Processes a single JSON file and inserts data into the database."""
    try:
        # Parse JSON data
        data = parse_json_data(file_path)

        # Connect to the database
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # Loop over each invoice and insert it sequentially
        for invoice in data.get("invoices", []):
            try:
                insert_invoice_data(connection, cursor, invoice)
                logging.info(f"Inserted invoice: {invoice['transaction_id']}")
            except Exception as e:
                logging.warning(
                    f"Retrying for invoice {invoice['transaction_id']}: {str(e)}")
                # Retry logic in case of failure
                try:
                    insert_invoice_data(connection, cursor, invoice)
                    logging.info(
                        f"Inserted invoice after retry: {invoice['transaction_id']}")
                except Exception as retry_error:
                    logging.error(
                        f"Failed after retry for invoice {invoice['transaction_id']}: {str(retry_error)}")

        cursor.close()
        connection.close()
        logging.info(f"Processing completed for file: {file_path}")

    except Exception as e:
        logging.critical(
            f"Critical error processing file {file_path}: {str(e)}")


if __name__ == "__main__":
    # Example usage
    FILE_PATH = "json_data/example_data.json"
    process_file(FILE_PATH)


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def populate_grant_total_data(batch_id, invoice_data, site_data, grand_totals):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    try:
        # Insert invoices data with check for duplicates
        for invoice in invoice_data:
            cursor.execute("""
                INSERT INTO invoices (batch_id, filename, payment_date, transaction_id, total)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING  -- Prevent duplicate transaction_id
            """, (batch_id, invoice['filename'], invoice['payment_date'], invoice['transaction_id'], invoice['total']))

        # Insert site totals data
        for site in site_data:
            cursor.execute("""
                INSERT INTO site_totals (batch_id, invoice_id, site_name, total)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (batch_id, invoice_id, site_name) DO NOTHING  -- Prevent duplicate site_totals
            """, (batch_id, site['invoice_id'], site['site_name'], site['total']))

        # Insert grand totals data
        for grand_total in grand_totals:
            cursor.execute("""
                INSERT INTO grand_totals (batch_id, site_name, total, total_of_grand_totals)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (batch_id, site_name) DO NOTHING  -- Prevent duplicate grand_totals
            """, (batch_id, grand_total['site_name'], grand_total['total'], grand_total['total_of_grand_totals']))

        connection.commit()
        print("Data populated successfully!")
        logging.info(f"Processing completed for file: {file_path}")

    except Exception as e:
        print(f"Error populating data: {e}")
        logging.critical(
            f"Critical error processing file {file_path}: {str(e)}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()
