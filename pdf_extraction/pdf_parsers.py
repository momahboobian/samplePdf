import re
from decimal import Decimal, ROUND_HALF_UP
import logging
from typing import Dict, List, Optional
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


def extract_site_totals_boom(pdf_text: str, site_names: List[str]) -> Dict[str, Decimal]:
    """
    Extracts site totals from the PDF text, specifically for the 'Boom_Facebook' format.

    Args:
        pdf_text (str): The extracted text from the PDF.
        site_names (List[str]): A list of site names to look for.

    Returns:
        Dict[str, Decimal]: A dictionary mapping site names to their totals.
    """
    matched_site_names: Dict[str, Decimal] = {}
    lines = pdf_text.split('\n')

    for i, line in enumerate(lines):
        if "Boom_Facebook" in line:
            # Find the site name, handling potential case differences
            site_name = next(
                (site for site in site_names if site.lower() in line.lower()), None
            )
            if site_name:
                # Look for the amount between "Boom" and "From" in the current or next line
                match = re.search(r'Boom.*?£(\d+\.\d{2}).*?From', line)
                if not match and i + 1 < len(lines):
                    match = re.search(r'£(\d+\.\d{2}).*?From', lines[i + 1])

                if match:
                    try:
                        amount = Decimal(match.group(1)).quantize(
                            Decimal("0.01"), rounding=ROUND_HALF_UP
                        )
                        matched_site_names[site_name] = (
                            matched_site_names.get(
                                site_name, Decimal(0)) + amount
                        )
                    except ValueError as e:
                        logger.error(
                            f"Error parsing amount in line '{line}': {e}"
                        )
                else:
                    logger.warning(
                        f"No valid amount found for site '{site_name}' in line: '{line}'"
                    )

    # Handle special case: "Leads" to "Leeds"
    if "Leads" in matched_site_names:
        matched_site_names["Leeds"] = (
            matched_site_names.get("Leeds", Decimal(0)) +
            matched_site_names["Leads"]
        )
        del matched_site_names["Leads"]

    logger.info(f"Extracted site totals: {matched_site_names}")
    return matched_site_names
