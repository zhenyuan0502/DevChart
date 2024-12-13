def remove_newlines_and_spacing(text):
    """
    Remove newlines and extra spaces from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text without newlines and extra spaces.
    """
    return text.replace("\n", "").strip()

def standardize_text(text):
    """
    Standardize the given text by removing newlines, extra spaces, and normalizing spacing.

    Args:
        text (str): The input text.

    Returns:
        str: The standardized text.
    """
    text = remove_newlines_and_spacing(text)
    text = " ".join(text.split())
    return text

from datetime import datetime, timezone

def unixtimestamp_to_date(timestamp):
    """
    Convert a Unix timestamp to a date string in the format 'YYYY-MM-DD'.

    Args:
        timestamp (int): The Unix timestamp.

    Returns:
        str: The date string in the format 'YYYY-MM-DD'.
    """
    ts = int(timestamp)
    return datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d')