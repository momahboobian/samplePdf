import os
import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdfs_path):
    text = ""
    with open(pdfs_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_numbers_from_text(text):
    pattern = r'From.*?£(\d+\.\d{2})' 
    numbers_in_text = re.findall(pattern, text)
    return numbers_in_text


def calculate_total_from_numbers(numbers_list):
    return sum(float(num) for num in numbers_list)


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_folder = os.path.join(current_dir, "uploads")

# Extract site text from the PDF
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        pdf_text = extract_text_from_pdf(pdf_path)
        print(f"Text from {filename}:\n{pdf_text}\n")
        
        # Extract numbers from the text
        numbers = extract_numbers_from_text(pdf_text)
        print(f"Numbers from {filename}:\n{numbers}\n")