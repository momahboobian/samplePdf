import re
import logging
from typing import Callable, Dict, List
from utils.logger import setup_logger
from decimal import Decimal
from .pdf_parsers import extract_site_totals_boom

setup_logger()
logger = logging.getLogger(__name__)


#  Define a type for the parser function
SiteTotalExtractor = Callable[[str, List[str]], Dict[str, Decimal]]

# Select which parser to use.
pdf_type_parsers: Dict[str, SiteTotalExtractor] = {
    "Boom_Facebook": extract_site_totals_boom,
    # Add other parsers here for different PDF types
}


def extract_site_totals(pdf_text: str, site_names: List[str], pdf_type: str = "Boom_Facebook") -> Dict[str, Decimal]:
    """
    Extracts site totals from the PDF text using the appropriate parser based on pdf_type.

    Args:
        pdf_text (str): The extracted text from the PDF.
        site_names (List[str]): A list of site names to look for.
        pdf_type (str, optional): The type of PDF to be parsed.
            Defaults to "Boom_Facebook".

    Returns:
        Dict[str, Decimal]: A dictionary mapping site names to their totals.
    """
    try:
        if not pdf_text or not site_names:
            logger.warning("PDF text or site names are missing.")
            return {}
        if pdf_type not in pdf_type_parsers:
            logger.warning(
                f"PDF type '{pdf_type}' not recognized. Defaulting to 'Boom_Facebook'.")
            pdf_type = "Boom_Facebook"

        parser = pdf_type_parsers.get(pdf_type)
        if parser:
            return parser(pdf_text, site_names)
        else:
            logger.error(f"No parser found for PDF type: {pdf_type}")
            return {}

    except Exception as e:
        logger.error(f"Error extracting site totals: {e}", exc_info=True)
        return {}


if __name__ == '__main__':
    # Example usage remains the same, but now it uses the modular approach
    sample_pdf_text = """
    Boom_Facebook_UK_Birmingham_B2C_Always On - 2024
    From Feb 1, 2025, 12:00 AM to Feb 3, 2025, 11:07 PM
    £48.86 GBP
    Boom_Facebook_UK_Lakeside_B2C_Always On - 2024
    From Feb 1, 2025, 12:00 AM to Feb 3, 2025, 11:07 PM
    £48.51 GBP
    Some other text
    Boom_Facebook_UK_Birmingham_B2C_Always On - 2024
    From Feb 1, 2025, 12:00 AM to Feb 3, 2025, 11:07 PM
    £99.99 GBP
    """
    site_names = ["Birmingham", "Lakeside", "Invalid Site"]
    site_totals = extract_site_totals(
        sample_pdf_text, site_names, pdf_type="Boom_Facebook")
    print("Site Totals:\n", site_totals)
