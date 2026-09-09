conversation_data = {}


def start_conversation(intent, details=None):
    global conversation_data

    if details is None:
        details = {}

    conversation_data = {
        "intent": intent,
        "details": details.copy()
    }

    return conversation_data


def update_conversation(new_details):
    global conversation_data

    if not conversation_data:
        return {}

    existing_details = conversation_data.get("details", {})

    for key, value in new_details.items():
        if value is not None:
            existing_details[key] = value

    conversation_data["details"] = existing_details

    return conversation_data


def get_conversation():
    return conversation_data


def clear_conversation():
    global conversation_data

    conversation_data = {}

    return conversation_data


if __name__ == "__main__":
    print("Starting conversation...")

    start_conversation(
        "SELL_GRAIN",
        {
            "grain_type": "Rice",
            "quantity": None,
            "location": None,
            "farmer_name": None
        }
    )

    print(get_conversation())

    print("\nAdding quantity and location...")

    update_conversation(
        {
            "quantity": 500,
            "location": "Bhimavaram"
        }
    )

    print(get_conversation())

    print("\nAdding farmer name...")

    update_conversation(
        {
            "farmer_name": "Ramesh"
        }
    )

    print(get_conversation())

    print("\nClearing conversation...")

    clear_conversation()

    print(get_conversation())