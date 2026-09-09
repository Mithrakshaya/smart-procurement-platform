import re


def extract_entities(message):

    # Handle empty messages
    if not message:
        return {
            "grain_type": None,
            "quantity": None,
            "location": None,
            "request_id": None
        }

    message_lower = message.lower()

    # -------------------------
    # Extract grain type
    # -------------------------
    grain_types = [
        "rice",
        "wheat",
        "maize",
        "corn",
        "paddy",
        "millet"
    ]

    grain_type = None

    for grain in grain_types:
        if grain in message_lower:
            grain_type = grain.capitalize()
            break

    # -------------------------
    # Extract quantity
    # -------------------------
    quantity = None

    words = message_lower.split()

    for index, word in enumerate(words):

        if word.isdigit():

            if index + 1 < len(words):
                next_word = words[index + 1]

                if next_word in [
                    "kg",
                    "kgs",
                    "kilogram",
                    "kilograms"
                ]:
                    quantity = int(word)
                    break

    # -------------------------
    # Extract location
    # -------------------------
    locations = [
        "bhimavaram",
        "hyderabad",
        "vijayawada",
        "visakhapatnam",
        "rajahmundry"
    ]

    location = None

    for city in locations:
        if city in message_lower:
            location = city.capitalize()
            break

    # -------------------------
    # Extract request ID
    # -------------------------

    request_id = None

    # Find IDs like REQ001, REQ002, REQ123, etc.
    match = re.search(
        r"\bREQ\d+\b",
        message,
        re.IGNORECASE
    )

    if match:
        request_id = match.group().upper()

    # -------------------------
    # Return all extracted entities
    # -------------------------

    return {
        "grain_type": grain_type,
        "quantity": quantity,
        "location": location,
        "request_id": request_id
    }


if __name__ == "__main__":

    test_messages = [

        "I want to sell 500 kg of rice from Bhimavaram",

        "I want to buy 300 kg wheat in Hyderabad",

        "I have maize to sell",

        "What is the status of request REQ002?",

        "Please track my request REQ003"
    ]

    for message in test_messages:

        result = extract_entities(message)

        print("Message:", message)
        print("Extracted Entities:", result)
        print("-" * 50)