from flask import Flask, request, jsonify, json
from flask_cors import CORS
import os
import re
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

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
    max_site_name_length = max(len(site) for site, _ in data)
    max_total_length = max(len(str(total)) for _, total in data)  # Convert total to string before getting length
    max_lengths = [max_site_name_length, max_total_length]

    row_format = " | ".join(["{:<" + str(length) + "}" for length in max_lengths])
    header = row_format.format("Site Name", "Total")
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for site_name, total in data:
        print(row_format.format(site_name, total))
    print(separator)


def calculate_totals_for_file(file_path):
    """
    Calculate total number of pages of a PDF file.

    Args:
        file_path (str): Path to the PDF file.

        Returns:
            dist: Dictionary containing calculated results.
    """
    pdf_text = extract_text_from_pdf(file_path)
    matched_site_names = extract_site_names_from_pdf(file_path)
    numbers = extract_numbers_from_text(pdf_text)

    # print("Matched site names:", matched_site_names)
    # print("Numbers:", numbers)

    if len(matched_site_names) != len(numbers):
        return jsonify({'error': 'Number of site names and numbers do not match'}), 400

    site_totals = {site: 0.0 for site in site_names}
    for site_name, price in zip(matched_site_names, numbers):
        price_float = float(price.replace('£', ''))
        site_totals[site_name] += price_float

    totals_data = [(site_name, "{:.2f}".format(total)) for site_name, total in site_totals.items()]
    grand_total = sum(site_totals.values())

    # print("\nCalculation Results:")
    # print_table(totals_data)
    # print("Grand Total: £{:.2f}\n".format(grand_total))

    return {
        'calculation_results': [{'site': site_name, 'total': total} for site_name, total in totals_data],
        'grand_total': "{:.2f}".format(grand_total),
        'totals': totals_data
    }


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and file.filename.endswith('.pdf'):
        uploads_folder = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)

        file_path = os.path.join(uploads_folder, file.filename)
        file.save(file_path)
        print("File saved successfully at:", file_path)

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format, must be a PDF'}), 400


@app.route('/action', methods=['POST'])
def perform_action():
    uploads_folder = os.path.join(os.getcwd(), 'uploads')
    files_in_folder = os.listdir(uploads_folder)
    calculation_results_all_files = []

    for file_name in files_in_folder:
        if file_name.endswith('.pdf'):
            file_path = os.path.join(uploads_folder, file_name)
            try:
                calculation_results = calculate_totals_for_file(file_path)
                calculation_results_all_files.append(calculation_results)
            except Exception as e:
                print(f"Error processing file {file_name}: {str(e)}")

    if not calculation_results_all_files:
        return jsonify({'error': 'No PDF files found or error processing files'}), 400

    grand_totals = {}
    for result in calculation_results_all_files:
        grand_total = float(result['grand_total'])
        for site_total in result['totals']:
            site_name, total = site_total
            if site_name not in grand_totals:
                grand_totals[site_name] = 0.0
            grand_totals[site_name] += float(total)

    print("\nGrand Totals of Sites:")
    print_table(list(grand_totals.items()))

    overall_grand_total = sum(grand_totals.values())
    print(f"Overall Grand Total: £{overall_grand_total:.2f}\n\n")

    def format_decimal_places(value):
        return "{:.2f}".format(value)

    # Modify the response data to format the numbers
    response_data = {
        'calculation_results': calculation_results_all_files,
        'grand_totals': {site: format_decimal_places(total) for site, total in grand_totals.items()},
        'overall_grand_total': format_decimal_places(sum(grand_totals.values()))
    }

    print("Response sent to frontend:", grand_totals)

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True)
