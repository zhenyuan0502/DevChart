

def remove_newlines_and_spacing(text):
    return text.replace("\n", "").strip()

def standardize_text(text):
    text = remove_newlines_and_spacing(text)
    text = " ".join(text.split())
    return text
    
from datetime import datetime, timezone
def unixtimestamp_to_date(timestamp):
    ts = int(timestamp)
    return datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d')