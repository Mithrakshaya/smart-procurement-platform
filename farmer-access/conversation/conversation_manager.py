conversation_state = {}


def start_conversation(intent, details):

    conversation_state["intent"] = intent
    conversation_state["details"] = details.copy()

    return conversation_state


def update_conversation(new_details):

    if "details" not in conversation_state:
        return None

    conversation_state["details"].update(
        new_details
    )

    return conversation_state


def get_conversation():

    return conversation_state


def clear_conversation():

    conversation_state.clear()


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

    print()

    print("Adding new information...")

    update_conversation(
        {
            "quantity": 500,
            "location": "Bhimavaram"
        }
    )

    print(get_conversation())

    print()

    print("Clearing conversation...")

    clear_conversation()

    print(get_conversation())