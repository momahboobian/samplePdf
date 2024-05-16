import logging
from PyPDF2 import PdfReader

site_names = {
    "Birmingham": "Birmingham",
    "Canterbury": "Canterbury",
    "Cardiff": "Cardiff",
    "Chelmsford": "Chelmsford",
    "Ealing": "Ealing",
    "Edinburgh": "Edinburgh",
    "Exeter": "Exeter",
    "Glasgow": "Glasgow",
    "Lakeside": "Lakeside",
    "Leeds": "Leeds",
    "Liverpool": "Liverpool",
    "Manchester": "Manchester",
    "Norwich": "Norwich",
    "Oxford Street": "Oxford Street",
    "Plymouth": "Plymouth",
    "Southend": "Southend",
    "Swindon": "Swindon",
    "The O2": "The O2",
    "Watford": "Watford",
    "Gifting": "Gifting",
    "St Patricks Day": "St Patricks Day",
}


def extract_site_names(pdf_path):
    """
    Extract site names from PDF text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: List of matched site names.
    """
    matched_site_names = []
    try:
        with open(pdf_path, "rb"):
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                lines = page.extract_text().split('\n')
                for line in lines:
                    if line.startswith("Boom"):
                        for site_name_key, site_name_value in site_names.items():
                            if site_name_value in line:
                                matched_site_names.append(site_name_key)
    except Exception as e:
        logging.error(f"Error extracting site names from PDF: {e}")
    return matched_site_names