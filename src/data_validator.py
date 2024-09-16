from datetime import datetime


def validate_date(date_str):
    """
    Validate and convert a date string to MySQL-compatible format (YYYY-MM-DD).
    Supports date formats like 'Sep 14'.
    Returns the converted date if valid, else None.
    """
    try:
        # Try to parse the date assuming format like 'Sep 14' (no year)
        date_obj = datetime.strptime(date_str, "%b %d")
        # Add current year if the year is missing
        date_obj = date_obj.replace(year=datetime.now().year)
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return None


def validate_status(status_str):
    """
    Validate status string ('TRUE'/'FALSE') and convert it to boolean.
    """
    if status_str == "TRUE":
        return True
    elif status_str == "FALSE":
        return False
    else:
        print(f"Invalid status value: {status_str}")
        return None
