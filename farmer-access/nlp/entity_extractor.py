def extract_entities(message):

    # Handle empty messages
    if not message:
        return {
            "grain_type": None,
            "quantity": None,
            "location": None
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

            # Check whether quantity is followed by kg
            if index + 1 < len(words):
                next_word = words[index + 1]

                if next_word in ["kg", "kgs", "kilogram", "kilograms"]:
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

    return {
        "grain_type": grain_type,
        "quantity": quantity,
        "location": location
    }


if __name__ == "__main__":

    test_messages = [
        "I want to sell 500 kg of rice from Bhimavaram",
        "I want to buy 300 kg wheat in Hyderabad",
        "I have maize to sell"
    ]

    for message in test_messages:

        result = extract_entities(message)

        print("Message:", message)
        print("Extracted Entities:", result)
        print("-" * 50)