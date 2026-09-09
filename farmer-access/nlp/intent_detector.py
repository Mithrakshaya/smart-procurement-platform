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
    test_message = "I want to buy wheat"

    result = detect_intent(test_message)

    print("Message:", test_message)
    print("Detected Intent:", result)