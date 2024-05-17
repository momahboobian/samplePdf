import re

def extract_numbers_from_text(text):
    pattern = r'From.*?£(\d+\.\d{2})' 
    numbers_in_text = re.findall(pattern, text)
    return numbers_in_text
