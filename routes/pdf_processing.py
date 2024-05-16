from flask import jsonify
import os
import logging

from utils.pdf_to_text import extract_text_from_pdf 
from utils.invoice_number import extract_invoice_number
from utils.site_names import extract_site_names, site_names
from utils.site_numbers import extract_site_numbers
from utils.totals_calculator import calculate_totals_for_file

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def perform_action():
    uploads_folder = os.path.join(os.getcwd(), 'uploads')
    files_in_folder = os.listdir(uploads_folder)
    calculation_results_all_files = []

    for file_name in files_in_folder:
        if file_name.endswith('.pdf'):
            file_path = os.path.join(uploads_folder, file_name)
            try:
                pdf_text = extract_text_from_pdf(file_path)
                matched_site_names = extract_site_names(file_path)
                numbers = extract_site_numbers(pdf_text)
                invoice_number = extract_invoice_number(pdf_text)
                
                calculation_results = calculate_totals_for_file(pdf_text, matched_site_names, numbers, invoice_number, site_names)
                if 'error' in calculation_results:
                    return jsonify(calculation_results), 400
                calculation_results_all_files.append(calculation_results)
            except Exception as e:
                logging.error(f"Error processing file {file_name}: {str(e)}")

    if not calculation_results_all_files:
        return jsonify({'error': 'No PDF files found or error processing files'}), 400

    grand_totals = {}
    for result in calculation_results_all_files:
        for site_total in result['totals']:
            site_name, total = site_total
            if site_name not in grand_totals:
                grand_totals[site_name] = 0.0
            grand_totals[site_name] += float(total)

    overall_grand_total = sum(grand_totals.values())
    logging.info(f"Overall Grand Total: £{overall_grand_total:.2f}\n\n")

    def format_decimal_places(value):
        return "{:.2f}".format(value)
    
    for result in calculation_results_all_files:
        del result['totals']

    response_data = [{
        'calculation_results': calculation_results_all_files,
        'grand_totals': {site: format_decimal_places(total) for site, total in grand_totals.items()},
        'overall_grand_total': format_decimal_places(sum(grand_totals.values()))
    }]

    return jsonify(response_data), 200