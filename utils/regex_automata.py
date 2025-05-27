import re

def validate_input(pattern: str, text: str) -> bool:
    return re.fullmatch(pattern, text) is not None

re.fullmatch(r"[A-Z]{1,2}\d{2,5}", id)
