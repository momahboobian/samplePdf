from PyPDF2 import PdfReader

def extract_text_from_pdf(pdfs_path):
    text = ""
    with open(pdfs_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text