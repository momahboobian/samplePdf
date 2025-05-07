from config import DATABASE_URL
import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()


schema = """
CREATE TABLE IF NOT EXISTS sites (
    id SERIAL,
    site_name VARCHAR(255) PRIMARY KEY,
    UNIQUE (site_name)
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL,
    invoice_identifier VARCHAR PRIMARY KEY,
    transaction_id VARCHAR,
    batch_id VARCHAR NOT NULL,
    processing_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS site_totals (
    id SERIAL,
    invoice_identifier VARCHAR NOT NULL REFERENCES invoices(invoice_identifier) ON DELETE CASCADE,
    site_name VARCHAR NOT NULL REFERENCES sites(site_name) ON DELETE CASCADE,
    total_amount DECIMAL NOT NULL,
    PRIMARY KEY (invoice_identifier, site_name)
);

CREATE TABLE IF NOT EXISTS grand_totals (
    id SERIAL,
    batch_id VARCHAR PRIMARY KEY,
    site_name VARCHAR NOT NULL REFERENCES sites(site_name) ON DELETE CASCADE,
    grand_total_amount DECIMAL NOT NULL,
    calculation_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (batch_id, site_name)
);

INSERT INTO sites (site_name)  -- Changed "name" to "site_name"
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

print("Database schema created successfully.")
