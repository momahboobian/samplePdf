def print_table(data):
    """
    Print data in a table format.

    Args:
        data (list): List of tuples representing data rows.
    """
    max_lengths = [max(len(str(cell)) for cell in col) for col in zip(*data)]
    row_format = " | ".join(["{:<" + str(length) + "}" for length in max_lengths])
    header = row_format.format(*data[0])
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for row in data[1:]:
        print(row_format.format(*row))
    print(separator)
