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


def calculate_total_from_numbers(numbers_list):
    """
    Calculate total from a list of numbers.

    Args:
        numbers_list (list): List of numbers.

    Returns:
        float: Total sum of numbers.
    """
    return sum(float(num) for num in numbers_list)


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_sample_path = os.path.join(current_dir, "media/sample.pdf")

# Extract site text from the PDF
pdf_text = extract_text_from_pdf(pdf_sample_path)
print(pdf_text)
