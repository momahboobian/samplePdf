import logging

def calculate_totals_for_file(pdf_text, matched_site_names, numbers, invoice_number, site_names):
    """
    Calculate total number of pages of a PDF file.

    Args:
        pdf_text (str): Text extracted from the PDF file.
        matched_site_names (list): List of matched site names.
        numbers (list): List of numbers extracted from the PDF text.
        invoice_number (str): Extracted invoice number.
        site_names (dict): Dictionary containing site names.

    Returns:
        dict: Dictionary containing calculated results.
    """
    try:
        if len(matched_site_names) != len(numbers):
            return {'error': 'Number of site names and numbers do not match'}

        site_totals = {site: 0.0 for site in site_names}
        for site_name, price in zip(matched_site_names, numbers):
            price_float = float(price.replace('£', ''))
            site_totals[site_name] += price_float

        totals_data = [(site_name, "{:.2f}".format(total)) for site_name, total in site_totals.items()]
        grand_total = sum(site_totals.values())

        return {
            'invoice_number': invoice_number,
            'sites_total_results': [{'site': site_name, 'total': total} for site_name, total in totals_data],
            'grand_total': "{:.2f}".format(grand_total),
            'totals': totals_data
        }

    except Exception as e:
        logging.error(f"Error calculating totals: {e}")
        return {'error': 'An error occurred while calculating totals'}
