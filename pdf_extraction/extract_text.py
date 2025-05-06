import os
import pdfplumber
import logging
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


def extract_text(pdf_path: str) -> str:
    """Extracts text content from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text, or an empty string if an error occurs.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        logger.info(f"Successfully extracted text from: {pdf_path}")
        return text
    except Exception as e:
        logger.error(
            f"Error extracting text from {pdf_path}: {e}", exc_info=True)
        return ""


if __name__ == '__main__':
    # Example usage (for testing)
    # Create a dummy PDF file for testing
    from io import BytesIO
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "This is a test PDF.")
    c.drawString(100, 700, "Another line of text.")
    c.save()
    buffer.seek(0)

    with open("test.pdf", "wb") as f:
        f.write(buffer.read())

    text = extract_text("test.pdf")
    print("Extracted Text:\n", text)

    os.remove("test.pdf")  # Clean up test file
