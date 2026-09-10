import re


# ============================================================
# VALID STATUSES
# ============================================================

VALID_STATUSES = {
    "REQUEST_CREATED",
    "UNDER_REVIEW",
    "MATCHED",
    "NEGOTIATION",
    "COMPLETED",
    "CANCELLED",
    "REJECTED",
}


STATUS_ALIASES = {
    "REQUEST CREATED": "REQUEST_CREATED",
    "CREATED": "REQUEST_CREATED",

    "UNDER REVIEW": "UNDER_REVIEW",
    "REVIEW": "UNDER_REVIEW",

    "MATCHED": "MATCHED",
    "MATCH": "MATCHED",

    "NEGOTIATION": "NEGOTIATION",
    "NEGOTIATE": "NEGOTIATION",

    "COMPLETED": "COMPLETED",
    "COMPLETE": "COMPLETED",
    "DONE": "COMPLETED",

    "CANCELLED": "CANCELLED",
    "CANCELED": "CANCELLED",
    "CANCEL": "CANCELLED",

    "REJECTED": "REJECTED",
    "REJECT": "REJECTED",
}


# ============================================================
# BASIC CLEANING
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def normalize_text(value):
    value = clean_text(value)

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.lower()


# ============================================================
# REQUEST ID
# ============================================================

def extract_request_id(text):
    match = re.search(
        r"\bREQ\d+\b",
        text,
        flags=re.IGNORECASE
    )

    if match:
        return match.group(0).upper()

    return None


# ============================================================
# STATUS
# ============================================================

def normalize_status(value):
    if value is None:
        return None

    value = clean_text(value)

    normalized = value.upper().replace("-", "_")

    if normalized in VALID_STATUSES:
        return normalized

    alias_key = value.upper()

    if alias_key in STATUS_ALIASES:
        return STATUS_ALIASES[alias_key]

    alias_key = alias_key.replace("_", " ")

    if alias_key in STATUS_ALIASES:
        return STATUS_ALIASES[alias_key]

    return normalized


def extract_status(text):
    normalized = normalize_text(text)

    # --------------------------------------------------------
    # Explicit status phrases
    # --------------------------------------------------------

    patterns = [
        r"(?:to|as|status(?:\s+to)?)\s+([a-zA-Z_ -]+)$",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            candidate = clean_text(
                match.group(1)
            )

            status = normalize_status(candidate)

            if status in VALID_STATUSES:
                return status

    # --------------------------------------------------------
    # Search known statuses
    # --------------------------------------------------------

    for status in VALID_STATUSES:

        readable = status.replace(
            "_",
            " "
        ).lower()

        if readable in normalized:
            return status

        if status.lower() in normalized:
            return status

    return None


# ============================================================
# QUANTITY
# ============================================================

def extract_quantity(text):

    patterns = [

        r"(\d+(?:\.\d+)?)\s*(?:kg|kgs|kilogram|kilograms)",

        r"(\d+(?:\.\d+)?)\s*(?:ton|tons|tonne|tonnes)",

        r"quantity\s*(?:is|of|:)?\s*(\d+(?:\.\d+)?)",

        r"\b(\d+(?:\.\d+)?)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            try:
                return float(
                    match.group(1)
                )

            except ValueError:
                pass

    return None


# ============================================================
# LOCATION
# ============================================================

def extract_location(text):

    patterns = [

        r"\bfrom\s+(.+?)(?=$|[,.])",

        r"\bat\s+(.+?)(?=$|[,.])",

        r"\bin\s+(.+?)(?=$|[,.])",

        r"location\s*(?:is|:)?\s*(.+)$",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            location = clean_text(
                match.group(1)
            )

            # Remove trailing conversational words.
            location = re.sub(
                r"\s+(?:and|with|for)\s*$",
                "",
                location,
                flags=re.IGNORECASE
            )

            if location:
                return location

    return None


# ============================================================
# PERSON NAME
# ============================================================

def extract_person_name(text):

    patterns = [

        r"\bmy name is\s+([A-Za-z][A-Za-z .'-]*)",

        r"\bname is\s+([A-Za-z][A-Za-z .'-]*)",

        r"\bi am\s+([A-Za-z][A-Za-z .'-]*)",

        r"\bi'm\s+([A-Za-z][A-Za-z .'-]*)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            name = clean_text(
                match.group(1)
            )

            # Prevent common trailing phrases.
            name = re.split(
                r"\s+(?:and|from|in|with|selling|buying)\b",
                name,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0]

            return name.strip()

    return None


# ============================================================
# PRODUCT
# ============================================================

def extract_product(text):

    original = clean_text(text)

    # --------------------------------------------------------
    # SELL
    # --------------------------------------------------------

    sell_patterns = [

        r"\bi\s+want\s+to\s+sell\s+"
        r"(?:\d+(?:\.\d+)?\s*)?"
        r"(?:kg|kgs|kilogram|kilograms|ton|tons|tonne|tonnes)?"
        r"\s*(?:of\s+)?(.+?)(?=\s+from\s+|\s+in\s+|\s+at\s+|$)",

        r"\bwant\s+to\s+sell\s+"
        r"(?:\d+(?:\.\d+)?\s*)?"
        r"(?:kg|kgs|kilogram|kilograms|ton|tons|tonne|tonnes)?"
        r"\s*(?:of\s+)?(.+?)(?=\s+from\s+|\s+in\s+|\s+at\s+|$)",

        r"\bsell\s+"
        r"(?:\d+(?:\.\d+)?\s*)?"
        r"(?:kg|kgs|kilogram|kilograms|ton|tons|tonne|tonnes)?"
        r"\s*(?:of\s+)?(.+?)(?=\s+from\s+|\s+in\s+|\s+at\s+|$)",
    ]

    # --------------------------------------------------------
    # BUY
    # --------------------------------------------------------

    buy_patterns = [

        r"\bi\s+want\s+to\s+buy\s+"
        r"(?:\d+(?:\.\d+)?\s*)?"
        r"(?:kg|kgs|kilogram|kilograms|ton|tons|tonne|tonnes)?"
        r"\s*(?:of\s+)?(.+?)(?=\s+from\s+|\s+in\s+|\s+at\s+|$)",

        r"\bwant\s+to\s+buy\s+"
        r"(?:\d+(?:\.\d+)?\s*)?"
        r"(?:kg|kgs|kilogram|kilograms|ton|tons|tonne|tonnes)?"
        r"\s*(?:of\s+)?(.+?)(?=\s+from\s+|\s+in\s+|\s+at\s+|$)",

        r"\bbuy\s+"
        r"(?:\d+(?:\.\d+)?\s*)?"
        r"(?:kg|kgs|kilogram|kilograms|ton|tons|tonne|tonnes)?"
        r"\s*(?:of\s+)?(.+?)(?=\s+from\s+|\s+in\s+|\s+at\s+|$)",
    ]

    all_patterns = (
        sell_patterns +
        buy_patterns
    )

    for pattern in all_patterns:

        match = re.search(
            pattern,
            original,
            flags=re.IGNORECASE
        )

        if match:

            product = clean_text(
                match.group(1)
            )

            product = re.sub(
                r"^(?:of|the)\s+",
                "",
                product,
                flags=re.IGNORECASE
            )

            product = re.sub(
                r"\s+$",
                "",
                product
            )

            if product:
                return product

    return None


# ============================================================
# INTENT DETECTION
# ============================================================

def is_update_status_request(text):

    normalized = normalize_text(text)

    # Explicit update phrases.
    if re.search(
        r"\b(update|change|modify|set)\b.*\bstatus\b",
        normalized
    ):
        return True

    # Mark request.
    if re.search(
        r"\bmark\s+REQ\d+\s+(?:as|to)\b",
        text,
        flags=re.IGNORECASE
    ):
        return True

    # REQ001 to COMPLETED
    if re.search(
        r"\bREQ\d+\s+(?:to|as)\s+",
        text,
        flags=re.IGNORECASE
    ):
        status = extract_status(text)

        if status:
            return True

    return False


def is_get_all_requests(text):

    normalized = normalize_text(text)

    patterns = [
        r"\b(get|show|list|view|display)\b.*\ball\b.*\brequests\b",
        r"\ball\b.*\brequests\b",
        r"\bget all requests\b",
    ]

    return any(
        re.search(pattern, normalized)
        for pattern in patterns
    )


def is_check_status_request(text):

    normalized = normalize_text(text)

    if re.search(
        r"\b(check|view|show|get)\b.*\bstatus\b",
        normalized
    ):
        return True

    if re.search(
        r"\bstatus\s+REQ\d+\b",
        text,
        flags=re.IGNORECASE
    ):
        return True

    if re.search(
        r"\bREQ\d+\s+status\b",
        text,
        flags=re.IGNORECASE
    ):
        return True

    return False


def is_buy_request(text):

    normalized = normalize_text(text)

    patterns = [
        r"\bi\s+want\s+to\s+buy\b",
        r"\bwant\s+to\s+buy\b",
        r"\bi\s+need\s+to\s+buy\b",
        r"\bneed\s+to\s+buy\b",
        r"\bbuy\b",
        r"\bpurchase\b"
    ]

    return any(
        re.search(pattern, normalized)
        for pattern in patterns
    )


def is_sell_request(text):

    normalized = normalize_text(text)

    patterns = [
        r"\bi\s+want\s+to\s+sell\b",
        r"\bwant\s+to\s+sell\b",
        r"\bi\s+need\s+to\s+sell\b",
        r"\bneed\s+to\s+sell\b",
        r"\bsell\b"
    ]

    return any(
        re.search(pattern, normalized)
        for pattern in patterns
    )


# ============================================================
# SPECIAL COMMAND
# ============================================================

def detect_special_command(text):

    normalized = normalize_text(text)

    if normalized in {
        "reset",
        "restart",
        "start over",
        "clear",
        "new request"
    }:
        return "RESET"

    if normalized in {
        "exit",
        "quit",
        "bye",
        "goodbye",
        "close"
    }:
        return "EXIT"

    return None


# ============================================================
# UPDATE STATUS PARSER
# ============================================================

def parse_update_status(text):

    request_id = extract_request_id(
        text
    )

    status = extract_status(
        text
    )

    return {
        "intent": "UPDATE_STATUS",
        "details": {
            "request_id": request_id,
            "status": status
        }
    }


# ============================================================
# CHECK STATUS PARSER
# ============================================================

def parse_check_status(text):

    request_id = extract_request_id(
        text
    )

    return {
        "intent": "CHECK_STATUS",
        "details": {
            "request_id": request_id
        }
    }


# ============================================================
# SELL / BUY PARSER
# ============================================================

def parse_sell_buy(text):

    sell = is_sell_request(
        text
    )

    buy = is_buy_request(
        text
    )

    if sell and not buy:

        intent = "SELL_GRAIN"

    elif buy and not sell:

        intent = "BUY_GRAIN"

    else:

        intent = None

    quantity = extract_quantity(
        text
    )

    location = extract_location(
        text
    )

    product = extract_product(
        text
    )

    person_name = extract_person_name(
        text
    )

    details = {
        "farmer_name": person_name,
        "buyer_name": person_name,
        "grain_type": product,
        "quantity": quantity,
        "location": location
    }

    return {
        "intent": intent,
        "details": details
    }


# ============================================================
# MAIN PARSER
# ============================================================

def parse_message(text):

    text = clean_text(text)

    if not text:

        return {
            "intent": None,
            "details": {}
        }

    # --------------------------------------------------------
    # SPECIAL COMMAND
    # --------------------------------------------------------

    special = detect_special_command(
        text
    )

    if special:

        return {
            "intent": special,
            "details": {}
        }

    # --------------------------------------------------------
    # UPDATE STATUS
    # --------------------------------------------------------

    if is_update_status_request(
        text
    ):

        return parse_update_status(
            text
        )

    # --------------------------------------------------------
    # GET ALL REQUESTS
    # --------------------------------------------------------

    if is_get_all_requests(text):

        return {
            "intent": "GET_ALL_REQUESTS",
            "details": {}
        }

    # --------------------------------------------------------
    # CHECK STATUS
    # --------------------------------------------------------

    if is_check_status_request(
        text
    ):

        return parse_check_status(
            text
        )

    # --------------------------------------------------------
    # SELL / BUY
    # --------------------------------------------------------

    return parse_sell_buy(
        text
    )


# ============================================================
# COMPATIBILITY ALIASES
# ============================================================

def smart_parse(text):
    """
    Main public parser function.
    """

    return parse_message(
        text
    )


def understand_message(text):
    """
    Compatibility alias.
    """

    return parse_message(
        text
    )


def smart_parse_message(text):
    """
    Compatibility alias for older code.

    This is intentionally defined here,
    not imported from this same module.
    """

    return parse_message(
        text
    )


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    tests = [

        "I want to sell 50 kg of tomatoes",

        "I want to buy 100 kg of red chillie",

        "Update status of REQ004 to UNDER_REVIEW",

        "Update status of REQ004 to MATCHED",

        "Change status of REQ004 to COMPLETED",

        "Mark REQ004 as NEGOTIATION",

        "REQ004 to COMPLETED",

        "status REQ004",

        "reset",

        "exit"
    ]

    print()
    print("=" * 70)
    print("SMART PARSER TEST")
    print("=" * 70)

    for test in tests:

        result = parse_message(
            test
        )

        print()
        print("INPUT :", test)
        print("OUTPUT:", result)

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)