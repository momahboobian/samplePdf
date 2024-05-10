import os
import re
from PyPDF2 import PdfReader

site_names = {
    "Birmingham": "Birmingham",
    "Canterbury": "Canterbury",
    "Cardiff": "Cardiff",
    "Chelmsford": "Chelmsford",
    "Ealing": "Ealing",
    "Edinburgh": "Edinburgh",
    "Exeter": "Exeter",
    "Glasgow": "Glasgow",
    "Lakeside": "Lakeside",
    "Leeds": "Leeds",
    "Liverpool": "Liverpool",
    "Manchester": "Manchester",
    "Norwich": "Norwich",
    "Oxford Street": "Oxford Street",
    "Plymouth": "Plymouth",
    "Southend": "Southend",
    "Swindon": "Swindon",
    "The O2": "The O2",
    "Watford": "Watford",
    "Gifting": "Gifting",
    "St Patricks Day": "St Patricks Day",
}

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

def extract_site_names_from_pdf(pdf_path):
    """
    Extract site names from PDF text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: List of matched site names.
    """
    matched_site_names = []
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            lines = page.extract_text().split('\n')
            for line in lines:
                if line.startswith("Boom"):
                    for site_name_key, site_name_value in site_names.items():
                        if site_name_value in line:
                            matched_site_names.append(site_name_key)
    return matched_site_names

def extract_numbers_from_text(text):
    """
    Extract numbers following '£' symbol from text.

    Args:
        text (str): Text to search for numbers.

    Returns:
        list: List of tuples containing site names and corresponding numbers.
    """
    pattern = r'From.*?£(\d+\.\d{2})'  # Updated regex pattern
    matches = re.findall(pattern, text)
    return matches

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def print_table(data):
    """
    Print data in a table format.

    Args:
        data (list): List of tuples representing data rows.
    """
    max_lengths = [max(len(str(cell)) for cell in col) for col in zip(*data)]
    row_format = " | ".join(["{:<" + str(length) + "}" for length in max_lengths])
    header = row_format.format(*data[0])
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for row in data[1:]:
        print(row_format.format(*row))
    print(separator)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_folder = os.path.join(current_dir, "media")  # Path to the folder containing PDF files

# Iterate through PDF files in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        pdf_text = extract_text_from_pdf(pdf_path)

        # Extract site names from the PDF
        matched_site_names = extract_site_names_from_pdf(pdf_path)

        # Extract numbers following '£' symbol from text
        numbers = extract_numbers_from_text(pdf_text)

        # Combine site names and numbers into rows for the table
        table_data = [("Site Name", "Price (£)")]
        site_totals = {site: 0 for site in site_names}  # Initialize site totals dictionary

        for site_name, price in zip(matched_site_names, numbers):
            price_float = float(price)  # Convert price string to float
            site_totals[site_name] += price_float  # Update site total
            table_data.append((site_name, "£" + price))

        # Print the invoice number
        invoice_number = extract_invoice_number(pdf_text)
        if invoice_number:
            print("Invoice/Receipt Number:", invoice_number)
            print()

        # Print the individual site prices table
        print("Individual Site Prices:")
        print_table(table_data)

        # Print the totals table
        totals_data = [("Site Name", "Total (£)")]
        for site_name, total in site_totals.items():
            totals_data.append((site_name, "£{:.2f}".format(total)))

        print("\nTotals:")
        print_table(totals_data)

        # Calculate total
        total = sum(float(num) for num in numbers)
        print("Invoice Total:", "£" + str(total))

        print("\n\n")
