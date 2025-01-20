import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL

def populate_data(batch_id, invoice_data, site_data, grand_totals):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    try:
        # Insert invoices data
        for invoice in invoice_data:
            cursor.execute("""
                INSERT INTO invoices (batch_id, filename, payment_date, transaction_id, total)
                VALUES (%s, %s, %s, %s, %s)
            """, (batch_id, invoice['filename'], invoice['payment_date'], invoice['transaction_id'], invoice['total']))

        # Insert site totals data
        for site in site_data:
            cursor.execute("""
                INSERT INTO site_totals (batch_id, invoice_id, site_name, total)
                VALUES (%s, %s, %s, %s)
            """, (batch_id, site['invoice_id'], site['site_name'], site['total']))

        # Insert grand totals data
        for grand_total in grand_totals:
            cursor.execute("""
                INSERT INTO grand_totals (batch_id, site_name, total, total_of_grand_totals)
                VALUES (%s, %s, %s, %s)
            """, (batch_id, grand_total['site_name'], grand_total['total'], grand_total['total_of_grand_totals']))

        connection.commit()
        print("Data populated successfully!")

    except Exception as e:
        print(f"Error populating data: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()
