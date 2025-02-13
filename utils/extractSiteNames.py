import re
import psycopg2
from decimal import Decimal, ROUND_HALF_UP
from config import DATABASE_URL

site_names_array = [
    "Aldgate",
    "Birmingham",
    "Brunch - 2024 – Conversion",
    "Bournemouth",
    "Cambridge",
    "Canterbury",
    "Cardiff",
    "Chelmsford",
    "Ealing",
    "Edinburgh",
    "Exeter",
    "Glasgow",
    "Ipswich",
    "Lakeside",
    "Leeds",
    "Leads",
    "Liverpool",
    "Manchester",
    "Norwich",
    "Oxford Street",
    "Plymouth",
    "Southampton",
    "Southend",
    "Swindon",
    "The O2",
    "Wandsworth",
    "Watford",
    "Gifting",
    "St Patricks Day",
]



def extract_site_names(pdf_text):
    # Connect to the database
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sites")
    site_names = [row[0] for row in cursor.fetchall()]
    connection.close()

    # print(site_names)

    matched_site_names = {}
    total_amount = Decimal(0)
    lines = pdf_text.split('\n')
    for i, line in enumerate(lines):
        if "Boom_Facebook" in line:
            site_name = next((site for site in site_names_array if site.lower() in line.lower()), None)
            if site_name:
                for j in range(i+1, len(lines)):
                    if "AM" in lines[j] or "PM" in lines[j]:
                        try:
                            amount = re.search(r'(\d+\.\d{2})', lines[j]).group(1)
                            amount = Decimal(amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                            matched_site_names[site_name] = matched_site_names.get(site_name, Decimal(0)) + amount
                            total_amount += amount
                        except AttributeError:
                            print(f"Error: Could not find amount in line '{lines[j]}'")
                        break
    # Add amounts for "Leads" to "Leeds"
    if "Leads" in matched_site_names:
        matched_site_names["Leeds"] = matched_site_names.get("Leeds", Decimal(0)) + matched_site_names["Leads"]
        del matched_site_names["Leads"]
    # print(matched_site_names)
    # print(f"Total Amount: {total_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")
    return matched_site_names