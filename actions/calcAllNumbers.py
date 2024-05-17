import os
import re
from PyPDF2 import PdfReader


def extract_numbers_from_text(text):
    """
    Extract numbers starting with '£' from text.

    Args:
        text (str): Text to search for numbers.

    Returns:
        list: List of numbers starting with '£'.
    """
    pattern = r'From.*?\d{2}:\d{2}£(\d+\.\d{2})'
    numbers_in_text = re.findall(pattern, text)
    return numbers_in_text


def extract_text_from_pdf(pdfs_path):
    """
    Extract text from a PDF file.

    Args:
        pdfs_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    with open(pdfs_path, "rb") as file:
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

# Example usage:
pdf_path = os.path.join(current_dir, "media/sample.pdf")
pdf_text = extract_text_from_pdf(pdf_path)

# Extract numbers starting with '£' from text
numbers = extract_numbers_from_text(pdf_text)

# Create data for the table
table_data = [("Numbers",)]
table_data.extend([("£" + num,) for num in numbers])

# Print the table
print_table(table_data)

# Calculate total
total = sum(float(num) for num in numbers)
print("Total:", "£" + str(total))
