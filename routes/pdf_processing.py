from flask import jsonify, request
import os
import logging
from utils.calcSiteTotals import calculate_site_totals
from utils.calcGrandTotals import calculate_grand_totals

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def perform_action(socketio):
    try:
        folder_name = request.args.get('folder_name')
        if not folder_name:
            return jsonify({'success': False, 'message': 'folder_name is required'}), 400

        upload_folder = os.path.join(os.getcwd(), 'uploads', folder_name)

        # Check if the folder exists
        if not os.path.exists(upload_folder):
            return jsonify({"error": "Folder not found"}), 404
        

        # Calculate site totals for all processed files
        site_totals = calculate_site_totals(upload_folder, socketio)

        # Calculate grand totals for all files
        grand_totals = calculate_grand_totals(upload_folder)

        # Prepare the final response
        response = {
            "site_totals": site_totals,
            "grand_totals": grand_totals,
        }


        return jsonify(response), 200

    except Exception as e:
        # Handle errors
        error_message = f"Error in perform_action (calculate_site_totals): {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500