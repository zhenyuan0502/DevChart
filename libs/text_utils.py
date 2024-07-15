

def remove_newlines_and_spacing(text):
    return text.replace("\n", "").strip()

def standardize_text(text):
    text = remove_newlines_and_spacing(text)
    text = " ".join(text.split())
    return text
    
    