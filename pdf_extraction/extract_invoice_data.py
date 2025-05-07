import re
import logging
from datetime import datetime
from decimal import Decimal
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


def extract_invoice_data(pdf_text: str) -> dict:
    """Extracts invoice-level data from the PDF text.

    Args:
        pdf_text (str): The extracted text from the PDF.

    Returns:
        dict: A dictionary containing invoice_id, payment_date, transaction_id,
              invoice_number, and total_paid.
              Returns an empty dictionary if extraction fails.
    """
    # how to add next line in print statement

    print("Extracting invoice data from PDF text...\n",  pdf_text)
    try:
        invoice_data = {}

        # Extract Reference Number
        ref_match = re.search(r"Reference number: ([A-Z0-9]+)", pdf_text)
        if ref_match:
            invoice_data['reference_number'] = ref_match.group(1).strip()
        else:
            logger.warning("Could not find reference_number in the PDF text.")
            invoice_data['reference_number'] = None

        # Extract Transaction ID
        trans_id_match = re.search(r"Transaction ID\s+([0-9\-]+)", pdf_text)
        if trans_id_match:
            invoice_data['transaction_id'] = trans_id_match.group(1).strip()
        else:
            logger.warning("Could not find transaction_id in the PDF text.")
            invoice_data['transaction_id'] = None

        # Extract Invoice Number
        invoice_num_match = re.search(r"Invoice no\. ([A-Z0-9\-]+)", pdf_text)
        if invoice_num_match:
            invoice_data['invoice_number'] = invoice_num_match.group(1).strip()
        else:
            logger.warning("Could not find invoice_number in the PDF text.")
            invoice_data['invoice_number'] = None

        # Extract Payment Date
        date_match = re.search(
            r"Invoice/payment date\s+([\d]{1,2} [A-Za-z]{3} [\d]{4})", pdf_text)
        if date_match:
            invoice_data['payment_date'] = date_match.group(1).strip()
        else:
            logger.warning("Could not find payment_date in the PDF text.")
            invoice_data['payment_date'] = None

        # Extract Total Paid
        total_paid_match = re.search(
            r"Reference number:.*?£([\d,.]+)", pdf_text)
        if total_paid_match:
            invoice_data['total_paid'] = f"£{total_paid_match.group(1).strip()}"
        else:
            logger.warning("Could not find total_paid in the PDF text.")
            invoice_data['total_paid'] = None

        return invoice_data

    except Exception as e:
        logger.error(f"Error extracting invoice data: {e}", exc_info=True)
        return {}
