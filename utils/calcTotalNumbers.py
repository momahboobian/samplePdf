def calculate_total_from_numbers(numbers_list):
    """
    Calculate total from a list of numbers.

    Args:
        numbers_list (list): List of numbers.

    Returns:
        float: Total sum of numbers.
    """
    return sum(float(num) for num in numbers_list)