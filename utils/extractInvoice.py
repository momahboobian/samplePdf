import re

def extract_invoice_number(text):
    """
    Extract invoice number from text.

    Args:
        text (str): Text to search for invoice number.

    Returns:
        str: Invoice number if found, else None.
    """
    pattern = r'Invoice/payment date\n(\d+ \w+ \d{4}, \d{2}:\d{2})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None