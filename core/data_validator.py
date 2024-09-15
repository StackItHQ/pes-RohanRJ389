# core/data_validator.py

def validate_data(row):
    """
    Validates a row of data to ensure it meets the criteria for insertion into the database.
    This is a simple example; modify as needed for your data.
    """
    if len(row) != 2:  # Assuming you have 2 columns, modify as necessary
        return False

    # Validate data types (e.g., first column is a string, second column is a number)
    if not isinstance(row[0], str):
        return False
    try:
        float(row[1])
    except ValueError:
        return False

    return True
