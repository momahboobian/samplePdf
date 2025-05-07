import os
import sys
import json
import logging
import psycopg2
from config import DATABASE_URL
from psycopg2 import sql
from utilsssss.json_parser import parse_json_data


def save_invoice_to_db(invoice_data, batch_id, filename):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Assuming invoice_data is a dictionary
                query = """
                    INSERT INTO invoices (batch_id, filename, payment_date, transaction_id, total)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """
                values = (batch_id, filename, invoice_data.get('payment_date'), invoice_data.get(
                    # Get data from invoice_data
                    'transaction_id'), invoice_data.get('total'))
                cur.execute(query, values)
                invoice_id = cur.fetchone()[0]  # Get the returned invoice ID
                conn.commit()
                return invoice_id  # Return the ID
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise  # Re-raise the exception


def save_grand_totals_to_db(grand_totals, batch_id):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                for site_name, total in grand_totals['grand_totals'].items():
                    query = """
                        INSERT INTO grand_totals (batch_id, site_name, total, total_of_grand_totals)
                        VALUES (%s, %s, %s, %s);
                    """
                    values = (batch_id, site_name, total,
                              grand_totals['total_of_grand_totals'])
                    cur.execute(query, values)
                conn.commit()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise

# ... (other database functions if needed)
