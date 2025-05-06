import os
import sys
import logging
import psycopg2
from config import DATABASE_URL

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
SITE_NAMES = [
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

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()


def create_tables():
    """Creates the necessary tables in the PostgreSQL database if they don't exist."""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create sites table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sites (
                id SERIAL PRIMARY KEY,
                site_name VARCHAR(255) UNIQUE NOT NULL
            )
        """)
        logging.info("Table 'sites' created or already exists.")

        # Create invoice_site_totals table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS invoice_site_totals (
                id SERIAL PRIMARY KEY,
                invoice_payment_date TIMESTAMP,
                reference_number VARCHAR(255),
                transaction_id VARCHAR(255),
                site_id INTEGER REFERENCES sites(id),
                site_total DECIMAL,
                invoice_number VARCHAR(255),
                total_paid DECIMAL
            )
        """)
        logging.info("Table 'invoice_site_totals' created or already exists.")

        conn.commit()
        logging.info("Database schema created successfully.")

    except psycopg2.Error as e:
        logging.error(f"Error creating tables: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()


def populate_sites_table():
    """Populates the 'sites' table with the initial list of site names if they don't exist."""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        for site_name in SITE_NAMES:
            cur.execute(
                "INSERT INTO sites (site_name) VALUES (%s) ON CONFLICT (site_name) DO NOTHING", (site_name,))

        conn.commit()
        logging.info(
            f"Sites table populated with {len(SITE_NAMES)} names (new ones added).")

    except psycopg2.Error as e:
        logging.error(f"Error populating sites table: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    create_tables()
    populate_sites_table()

# Execute schema creation
# cursor.execute(schema)
connection.commit()
cursor.close()
connection.close()

print("Database schema created successfully.")
