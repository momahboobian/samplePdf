import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL


connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

schema = """
CREATE TABLE IF NOT EXISTS sites (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    batch_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    payment_date TIMESTAMP,
    transaction_id TEXT UNIQUE,
    total NUMERIC
);

CREATE TABLE IF NOT EXISTS site_totals (
    id SERIAL PRIMARY KEY,
    batch_id TEXT NOT NULL,
    invoice_id INT REFERENCES invoices(id),
    site_name TEXT NOT NULL,
    total NUMERIC
);

CREATE TABLE IF NOT EXISTS grand_totals (
    id SERIAL PRIMARY KEY,
    batch_id TEXT NOT NULL,
    site_name TEXT NOT NULL,
    total NUMERIC,
    total_of_grand_totals NUMERIC
);

INSERT INTO sites (name)
VALUES
    ('Aldgate'),
    ('Birmingham'),
    ('Brunch - 2024 – Conversion'),
    ('Bournemouth'),
    ('Cambridge'),
    ('Canterbury'),
    ('Cardiff'),
    ('Chelmsford'),
    ('Ealing'),
    ('Edinburgh'),
    ('Exeter'),
    ('Glasgow'),
    ('Ipswich'),
    ('Lakeside'),
    ('Leeds'),
    ('Liverpool'),
    ('Manchester'),
    ('Norwich'),
    ('Oxford Street'),
    ('Plymouth'),
    ('Southampton'),
    ('Southend'),
    ('Swindon'),
    ('The O2'),
    ('Wandsworth'),
    ('Watford'),
    ('Gifting'),
    ('St Patricks Day');
"""

# Execute schema creation
cursor.execute(schema)
connection.commit()
cursor.close()
connection.close()
