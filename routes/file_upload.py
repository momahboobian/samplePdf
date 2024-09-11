from flask import jsonify, request
import os
import time
import logging
from .pdf_processing import calculate_site_totals, calculate_grand_totals

# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

 # Create a timestamped folder for this upload session
timestamp = time.strftime("%Y%m%d_%H%M%S")
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', timestamp)

# Set up logging
logging.basicConfig(level=logging.DEBUG)


def upload_file(socketio):
    try:

       

        
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        files = request.files.getlist('files[]')
        total_files = len(files)
        processed_files = 0
        grand_total = 0

        if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)


        for file in files:
            if file and file.filename.endswith('.pdf'):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                logging.info(f"File saved successfully at: {file_path}")

                invoice_total = process_invoice(file_path) 
                grand_total += invoice_total

                processed_files += 1

                # Emit WebSocket event to the client
                socketio.emit('invoice_processed', {
                    'file': file.filename,
                    'total': invoice_total,
                    'progress': processed_files / total_files * 100
                })
            else:
                return jsonify({'error': 'Invalid file format, must be a PDF'}), 400

        # Emit WebSocket event for grand total
        socketio.emit('processing_complete', {'grand_total': grand_total})

        return jsonify({'message': 'Files uploaded successfully'}), 200
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500


def process_invoice(file_path: str):
    try:
        # Extract and process invoice data using the actual logic
        site_totals = calculate_site_totals(UPLOAD_FOLDER)
        grand_totals = calculate_grand_totals(UPLOAD_FOLDER)
        
        # Assume the grand total is what you need to return
        return float(grand_totals['total_of_grand_totals'])
    
    except Exception as e:
        logging.error(f"Error processing invoice at {file_path}: {e}")
        return 0.0  # Or handle according to your error management strategy
