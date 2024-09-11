from flask import jsonify, request
import os
import time
import logging

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

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

        for file in files:
            if file and file.filename.endswith('.pdf'):
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{file.filename}"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
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


def process_invoice(file_path):
    # Mock implementation, replace with actual PDF processing logic
    # Assume each invoice has a random total between 100 and 500
    import random
    invoice_total = random.randint(100, 500)
    return invoice_total