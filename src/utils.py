import re

def sanitize_filename(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", text)[:50]
