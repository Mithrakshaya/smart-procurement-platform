def detect_intent(message):
    message = message.lower()

    if any(word in message for word in ["sell", "selling"]):
        return "SELL_GRAIN"

    elif any(word in message for word in ["buy", "purchase"]):
        return "BUY_GRAIN"

    elif any(word in message for word in ["status", "track"]):
        return "CHECK_STATUS"

    else:
        return "UNKNOWN"


if __name__ == "__main__":

    test_messages = [
        "I want to sell my rice",
        "I want to buy wheat",
        "I want to track my order",
        "Hello, I need some help"
    ]

    for message in test_messages:
        result = detect_intent(message)

        print("Message:", message)
        print("Detected Intent:", result)
        print("-" * 40)