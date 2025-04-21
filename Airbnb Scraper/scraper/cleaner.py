import re

def clean_text(text):
    if not text:
        return ""
    return text.strip().replace('\n', ' ').replace('\r', '').rstrip('.')

def clean_hosted_by(text):
    if not text:
        return ""
    text = text.replace("Hosted by", "").strip()
    return re.sub(r'\s+', ' ', text)

def clean_rules(raw_text):
    house_rules = []
    additional_rules = []

    if not raw_text:
        return {"house_rules": "", "additional_rules": ""}

    # Split by commas or newlines
    lines = re.split(r'[,\n]', raw_text)
    in_additional = False

    for line in lines:
        clean_line = re.sub(r'\s+', ' ', line.strip().rstrip('.'))
        if not clean_line:
            continue

        # Trigger switch to additional rules
        if "additional rules" in clean_line.lower():
            in_additional = True
            continue

        if clean_line.lower() in ["show more", "additional requests"]:
            continue

        if re.match(r"^\d+\.", clean_line):  # e.g. "1. No parties"
            in_additional = True

        if in_additional:
            additional_rules.append(clean_line)
        else:
            house_rules.append(clean_line)

    return {
        "house_rules": ", ".join(dict.fromkeys(house_rules)),
        "additional_rules": ", ".join(dict.fromkeys(additional_rules)),
    }


def clean_amenities(raw_text):
    available = []
    unavailable = []
    items = [i.strip() for i in raw_text.split(",") if i.strip()]

    for item in items:
        if item.startswith("Unavailable:"):
            cleaned = item.replace("Unavailable:", "").strip()
            cleaned = re.sub(r"\bThis place.*$", "", cleaned).strip()
            cleaned = remove_repeated_substring(cleaned)
            unavailable.append(cleaned)
        elif "This place may" in item:
            continue
        else:
            cleaned = remove_repeated_substring(item.strip())
            available.append(cleaned)

    return {
        "available": list(set(available)),
        "unavailable": list(set(unavailable))
    }

def remove_repeated_substring(text):
    mid = len(text) // 2
    for i in range(1, mid + 1):
        prefix = text[:i]
        if prefix * 2 == text:
            return prefix
    return text

def extract_number(text):
    if not text:
        return ""
    match = re.search(r'\d+\.?\d*', text)
    return match.group() if match else ""

def extract_rating(text):
    if not text:
        return ""
    match = re.search(r'(\d+\.\d+)', text)
    return match.group(1) if match else extract_number(text)
