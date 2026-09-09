def detect_farmer_intent(message):
    message = message.lower()

    if any(word in message for word in ["sell", "selling", "price"]):
        return "SELL_GRAIN"

    elif any(word in message for word in ["buy", "purchase"]):
        return "BUY_GRAIN"

    elif any(word in message for word in ["status", "order", "request"]):
        return "CHECK_STATUS"

    else:
        return "UNKNOWN"


def process_farmer_voice(message):

    if not message:
        return {
            "success": False,
            "message": "No voice message received"
        }

    intent = detect_farmer_intent(message)

    return {
        "success": True,
        "original_message": message,
        "detected_intent": intent,
        "message": "Farmer request processed successfully"
    }


if __name__ == "__main__":
    test_message = "I want to sell my rice"

    result = process_farmer_voice(test_message)

    print(result)