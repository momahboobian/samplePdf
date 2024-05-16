import re

def extract_site_numbers(text):
    """
    Extract numbers following '£' symbol from text.

    Args:
        text (str): Text to search for numbers.

    Returns:
        list: List of tuples containing site names and corresponding numbers.
    """
    pattern = r'From.*?£(\d+\.\d{2})'
    matches = re.findall(pattern, text)
    return matches