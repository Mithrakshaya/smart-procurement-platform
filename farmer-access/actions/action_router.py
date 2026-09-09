def route_action(intent):

    if intent == "SELL_GRAIN":
        return {
            "action": "SELL_GRAIN",
            "response": "Starting the grain selling process"
        }

    elif intent == "BUY_GRAIN":
        return {
            "action": "BUY_GRAIN",
            "response": "Starting the grain buying process"
        }

    elif intent == "CHECK_STATUS":
        return {
            "action": "CHECK_STATUS",
            "response": "Checking your request status"
        }

    else:
        return {
            "action": "UNKNOWN",
            "response": "Sorry, I could not understand your request"
        }


if __name__ == "__main__":

    test_intents = [
        "SELL_GRAIN",
        "BUY_GRAIN",
        "CHECK_STATUS",
        "UNKNOWN"
    ]

    for intent in test_intents:
        result = route_action(intent)
        print(intent, "→", result)