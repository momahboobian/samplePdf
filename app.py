import PyPDF2


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
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text


# Example usage:
pdf_path = "example.pdf"  # Replace "example.pdf" with the path to your PDF file
pdf_text = extract_text_from_pdf(pdf_path)
print(pdf_text)
