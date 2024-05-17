from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import time
import shutil
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')


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
    pattern = r'From.*?£(\d+\.\d{2})'
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


def is_upload_folder_empty():
    return not os.path.isdir(UPLOAD_FOLDER)


def empty_upload_folder():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('files[]')

    if is_upload_folder_empty():
        return jsonify({'error': 'Upload folder is not empty. Do you want to empty it?'}), 409

    for file in files:
        if file and file.filename.endswith('.pdf'):
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            print("File saved successfully at:", file_path)
        else:
            return jsonify({'error': 'Invalid file format, must be a PDF'}), 400

    return jsonify({'message': 'Files uploaded successfully'}), 200



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
        for site_total in result['totals']:
            site_name, total = site_total
            if site_name not in grand_totals:
                grand_totals[site_name] = 0.0
            grand_totals[site_name] += float(total)

    # print("\nGrand Totals of Sites:")
    # print_table(list(grand_totals.items()))

    overall_grand_total = sum(grand_totals.values())
    print(f"Overall Grand Total: £{overall_grand_total:.2f}\n\n")

    def format_decimal_places(value):
        return "{:.2f}".format(value)

    # Modify the response data to format the numbers
    response_data = [{
        # 'calculation_results': calculation_results_all_files,
        'grand_totals': {site: format_decimal_places(total) for site, total in grand_totals.items()},
        'overall_grand_total': format_decimal_places(sum(grand_totals.values()))
    }]

    print("Response sent to frontend:", response_data)

    return jsonify(response_data), 200


@app.route('/empty', methods=['POST'])
def empty_folder():
    if request.method == 'POST':
        confirmation = request.json.get('confirmation', False)
        if confirmation:
            empty_upload_folder()
            return jsonify({'message': 'Upload folder emptied successfully.'}), 200
        else:
            return jsonify({'error': 'Confirmation not received. Please confirm to empty the folder.'}), 400
    else:
        return jsonify({'error': 'Method not allowed. Please use POST method.'}), 405


@app.route('/check-folder', methods=['GET'])
def check_folder():
    folder_empty = is_upload_folder_empty()
    return jsonify({'folder_empty': folder_empty})


if __name__ == '__main__':
    app.run(debug=True)
