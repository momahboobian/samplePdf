import re

def extract_invoice_number(text):
    # invoice number
    invoice_pattern = r'Invoice/Payment Date\s+([A-Za-z]{3} \d{1,2}, \d{4}, \d{1,2}:\d{2} [AP]M)'
    invoice_match = re.search(invoice_pattern, text)
    payment_date = invoice_match.group(1) if invoice_match else None

    # transaction ID
    transaction_pattern = r'Transaction ID\s+(\d+-\d+)'
    transaction_match = re.search(transaction_pattern, text)
    transaction_id = transaction_match.group(1) if transaction_match else None

    return {
        'payment_date': payment_date,
        'transaction_id': transaction_id
    }