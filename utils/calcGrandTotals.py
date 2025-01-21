import os
from collections import defaultdict
from utils.extractText import extract_text_from_pdf
from utils.extractSiteNames import extract_site_names
from utils.printTable import print_table


def calculate_grand_totals(pdf_folder):
    grand_totals = defaultdict(float)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            pdf_text = extract_text_from_pdf(pdf_path)
            matched_site_names = extract_site_names(pdf_text)

            for site_name, number in matche:
                grand_totals[site_name] += float(number)

    # Print grand totals
    # print("Grand Totals:")
    # table_data = [("Site Name", "Price (£)")]

    # total_grand_total = 0.0
    # formatted_grand_totals = {}
    # for site_name, total_amount in grand_totals.items():
    #     table_data.append((site_name, f"{total_amount:.2f}"))
    #     formatted_grand_totals[site_name] = f"{total_amount:.2f}"
    #     total_grand_total += total_amount
    
    # Print total of grand totals
    # print_table(table_data)
    # print(f"Total of Grand Totals: £{total_grand_total:.2f}")


    formatted_grand_totals = {site_name: f"{amount:.2f}" for site_name, amount in grand_totals.items()}
    total_of_grand_totals = sum(grand_totals.values())

    return {
        "grand_totals": formatted_grand_totals,
        "total_of_grand_totals": f"{total_of_grand_totals:.2f}"
    }




