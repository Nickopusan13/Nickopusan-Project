import re

def clean_phone(text):
    if not text:
        return ""
    if re.fullmatch(r"\(\d{3}\) \d{3}-\d{4}", text.strip()):
        return text.strip()
    digits = re.sub(r'\D', '', text.replace("tel:", "").strip())
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    
    return text
