import re


def detect_document_type(text):

    text_upper = text.upper()

    if re.search(r"\b\d{12}\b|\b\d{4}\s\d{4}\s\d{4}\b", text):
        return "AADHAAR"

    if re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text):
        return "PAN"

    if "PASSPORT" in text_upper:
        return "PASSPORT"

    if "DRIVING" in text_upper or "DL NO" in text_upper:
        return "DRIVING_LICENSE"

    if re.search(r"[A-Z]{3}[0-9]{7}", text):
        return "VOTER_ID"

    return "UNKNOWN"


def extract_name(lines):

    for i, line in enumerate(lines):

        if re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", line):

            for j in range(i - 1, max(i - 4, -1), -1):

                candidate = lines[j]

                if len(candidate) > 3 and not re.search(r"\d", candidate):

                    return candidate

    return None


def extract_dob(text):

    dob_match = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)

    if dob_match:
        return dob_match.group()

    dob_match2 = re.search(r"\b\d{2}-\d{2}-\d{4}\b", text)

    if dob_match2:
        return dob_match2.group()

    return None


def extract_phone(text):

    phone_match = re.search(r"\b[6-9]\d{9}\b", text)

    if phone_match:
        return phone_match.group()

    return None


def extract_email(text):

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email_match:
        return email_match.group()

    return None


def extract_document_number(text, doc_type):

    if doc_type == "AADHAAR":

        match = re.search(r"\b\d{12}\b|\b\d{4}\s\d{4}\s\d{4}\b", text)
        return match.group() if match else None

    if doc_type == "PAN":

        match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
        return match.group() if match else None

    if doc_type == "PASSPORT":

        match = re.search(r"[A-Z][0-9]{7}", text)
        return match.group() if match else None

    if doc_type == "DRIVING_LICENSE":

        match = re.search(r"[A-Z]{2}[0-9]{2}\s?[0-9]{11}", text)
        return match.group() if match else None

    if doc_type == "VOTER_ID":

        match = re.search(r"[A-Z]{3}[0-9]{7}", text)
        return match.group() if match else None

    return None


def extract_address(lines):

    address_lines = []
    capture = False

    for line in lines:

        line_upper = line.upper()

        if "ADDRESS" in line_upper or "पता" in line_upper:
            capture = True
            continue

        if capture:

            if len(line.strip()) < 3:
                break

            address_lines.append(line)

    if address_lines:
        return " ".join(address_lines)

    return None


def extract_expiry(text):

    match = re.search(r"EXP.*\d{2}/\d{2}/\d{4}", text)

    if match:

        date = re.search(r"\d{2}/\d{2}/\d{4}", match.group())

        if date:
            return date.group()

    return None


def extract_fields(text):

    result = {}

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Detect Document Type
    doc_type = detect_document_type(text)

    # Extract fields
    name = extract_name(lines)

    dob = extract_dob(text)

    phone = extract_phone(text)

    email = extract_email(text)

    document_number = extract_document_number(text, doc_type)

    address = extract_address(lines)

    expiry = extract_expiry(text)

    result["DocumentType"] = doc_type
    result["Name"] = name
    result["DateOfBirth"] = dob
    result["Phone"] = phone
    result["Email"] = email
    result["DocumentNumber"] = document_number
    result["Address"] = address
    result["ExpiryDate"] = expiry

    return result