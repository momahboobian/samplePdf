import re

def extract_invoice_number(text):
    pattern = r'Invoice/payment date\n(\d+ \w+ \d{4}, \d{2}:\d{2})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None