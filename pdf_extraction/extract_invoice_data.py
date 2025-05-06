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
        dict: A dictionary containing invoice_payment_date, reference_number,
              transaction_id, invoice_number, and total_paid.
              Returns an empty dictionary if extraction fails.
    """
    invoice_data = {}
    try:
        # Extract Invoice/Payment Date
        date_match = re.search(r"Invoice/Payment Date\n(.*)", pdf_text)
        if date_match:
            date_str = date_match.group(1).strip()
            try:
                # Attempt to parse with different formats
                formats = ["%b %d, %Y, %I:%M %p", "%d %b %Y, %H:%M"]
                for fmt in formats:
                    try:
                        invoice_data['invoice_payment_date'] = datetime.strptime(
                            date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    logger.warning(f"Could not parse invoice date: {date_str}")
                    invoice_data['invoice_payment_date'] = None
            except Exception as e:
                logger.error(f"Error parsing invoice date '{date_str}': {e}")
                invoice_data['invoice_payment_date'] = None

        # Extract Reference Number
        ref_match = re.search(r"Reference Number: (.*)", pdf_text)
        if ref_match:
            invoice_data['reference_number'] = ref_match.group(1).strip()

        # Extract Transaction ID
        trans_id_match = re.search(r"Transaction ID\n(.*)", pdf_text)
        if trans_id_match:
            invoice_data['transaction_id'] = trans_id_match.group(1).strip()

        # Extract Invoice Number (using the format from the sample)
        invoice_num_match = re.search(r"Invoice #([A-Z0-9-]+)", pdf_text)
        if invoice_num_match:
            invoice_data['invoice_number'] = invoice_num_match.group(1).strip()

        # Extract Total Paid
        total_paid_match = re.search(r"Paid\n(£[\d,.]+ GBP)", pdf_text)
        if total_paid_match:
            total_str = total_paid_match.group(1).replace(
                '£', '').replace(' GBP', '').replace(',', '')
            try:
                invoice_data['total_paid'] = Decimal(
                    total_str).quantize(Decimal('0.01'))
            except ValueError:
                logger.error(f"Could not parse total paid: {total_str}")
                invoice_data['total_paid'] = None

        logger.info(f"Extracted invoice data: {invoice_data}")
        return invoice_data

    except Exception as e:
        logger.error(f"Error extracting invoice data: {e}", exc_info=True)
        return {}


if __name__ == '__main__':
    # Example usage (replace with actual PDF text for testing)
    sample_pdf_text = """
    Invoice for Boom: Battle Bar UK
    Account ID: 669990227174419

    Invoice/Payment Date
    Feb 3, 2025, 11:08 PM

    Payment method
    Visa 3024

    Reference Number: MUGG2G4S22

    Transaction ID
    9021916131251827-8825831227526982

    Product Type
    Meta adsPaid
    £1,556.00 GBP
    You're being billed because you reached your £1,556.00 payment threshold.
    Meta Platforms Ireland Limited
    Invoice # FBADS-020-104172678
    """
    invoice_data = extract_invoice_data(sample_pdf_text)
    print("Invoice Data:\n", invoice_data)

    sample_pdf_text_2 = """
    Invoice for Boom: Battle Bar UK
    Invoice/payment date
    31 Mar 2025, 18:42
    Reference number. GYNHRKGS22
    Transaction ID
    9282596088517166-9121823384594436
    Paid
    £1,234.56 GBP
    Invoice no. FBADS-020-104353386
    """
    invoice_data_2 = extract_invoice_data(sample_pdf_text_2)
    print("Invoice Data 2:\n", invoice_data_2)
