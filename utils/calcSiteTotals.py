import os
from collections import defaultdict
from utils.extractText import extract_text_from_pdf
from utils.extractInvoice import extract_invoice_number
from utils.extractSiteNames import extract_site_names
from utils.printTable import print_table

def calculate_site_totals(upload_folder, socketio=None):
    site_totals = defaultdict(lambda: defaultdict(float))
    total_files = len([f for f in os.listdir(upload_folder) if f.endswith('.pdf')])
    processed_files = 0

    for filename in os.listdir(upload_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(upload_folder, filename)
            pdf_text = extract_text_from_pdf(pdf_path)
            invoice_number = extract_invoice_number(pdf_text)
            matched_site_names = extract_site_names(pdf_text)
            pdf_site_totals = defaultdict(float)

            for site_name, total_amount in matched_site_names.items():
                pdf_site_totals[site_name] = round(pdf_site_totals.get(site_name, 0) + float(total_amount), 2)

            total = sum(pdf_site_totals.values())

            site_totals[filename] = {
                "invoice": invoice_number,
                'sites_totals': dict(pdf_site_totals),
                "total": total
            }

            if socketio:
                processed_files += 1
                # Emit real-time progress
                socketio.emit('invoice_processed', {
                    'file': filename,
                    'invoice': invoice_number,
                    'site_totals': dict(pdf_site_totals),
                    'total': total,
                    'progress': (processed_files / total_files) * 100
                })
            
            # Print the table
            table_data = [("Site Name", "Price (£)")]
            for site_name, price in pdf_site_totals.items():
                table_data.append((site_name, "£" + str(price)))
            print_table(table_data)
            print("Total:", "£" + str(total))

    return site_totals