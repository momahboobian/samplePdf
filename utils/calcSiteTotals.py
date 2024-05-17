import os
from collections import defaultdict
from utils.extractText import extract_text_from_pdf
from utils.extractNumbers import extract_numbers_from_text
from utils.extractInvoice import extract_invoice_number
from utils.calcTotalNumbers import calculate_total_from_numbers
from utils.extractSiteNames import extract_site_names, site_names
from utils.printTable import print_table


def calculate_site_totals(pdf_folder):
    site_totals = defaultdict(dict)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            pdf_text = extract_text_from_pdf(pdf_path)
            invoice_number = extract_invoice_number(pdf_text)
            numbers = extract_numbers_from_text(pdf_text)
            matched_site_names = extract_site_names(pdf_text, site_names)
            pdf_site_totals = defaultdict(float)

            for site_name, number in matched_site_names:
                pdf_site_totals[site_name] += float(number)

            total = calculate_total_from_numbers(numbers)

            # Prepare data for table
            table_data = [("Site Name", "Price (£)")]
            table_data.extend([(site_name, f"{total_amount:.2f}") for site_name, total_amount in pdf_site_totals.items()])


            # Print information
            print(f"\nInvoice Number: {invoice_number}\n")
            print(f"File Name: {filename}\n")

            # Print site totals for the current PDF file
            # print("Site Totals:")
            # for site_name, total_amount in pdf_site_totals.items():
            #     print(f"{site_name}: £{total_amount:.2f}")

            print_table(table_data)

            # Print the total for the current PDF file
            print(f"Total for Invoice: {invoice_number}: £{total:.2f}\n*****--------------******\n")

            site_totals[filename] = {
                "invoice_number": invoice_number,
                "site_totals": {site_name: f"{total_amount:.2f}" for site_name, total_amount in pdf_site_totals.items()},
                "total": f"{total:.2f}",
            }

    return site_totals
