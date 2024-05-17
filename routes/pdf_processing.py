import logging
from flask import jsonify

from utils.calcSiteTotals import calculate_site_totals
from utils.calcGrandTotals import calculate_grand_totals

# Set up logging
logging.basicConfig(level=logging.DEBUG)

pdf_folder = "uploads"

def perform_action():
    try:
        # Calculate site totals for each PDF file in the folder
        site_totals = calculate_site_totals(pdf_folder)

        # Calculate grand totals for each site across all PDFs in the folder
        grand_totals = calculate_grand_totals(pdf_folder)

        # Prepare response JSON
        response = {"site_totals": site_totals, "grand_totals": grand_totals}

        return jsonify(response), 200
    except Exception as e:
        # Handle errors and return error response
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500