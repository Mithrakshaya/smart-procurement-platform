import sys
import os


# Get the main farmer-access folder path
base_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

nlp_path = os.path.join(base_path, "nlp")
actions_path = os.path.join(base_path, "actions")
conversation_path = os.path.join(base_path, "conversation")


# Add folders to Python path
sys.path.append(nlp_path)
sys.path.append(actions_path)
sys.path.append(conversation_path)


# Import required modules
from intent_detector import detect_intent
from entity_extractor import extract_entities
from missing_info_detector import find_missing_information
from action_router import route_action

from conversation_manager import (
    start_conversation,
    update_conversation,
    get_conversation,
    clear_conversation
)


def extract_name(message, intent):

    words = message.strip().split()

    # If the user provides only one word,
    # treat it as a name during an active conversation
    if len(words) == 1 and words[0].isalpha():

        if intent == "SELL_GRAIN":
            return {
                "farmer_name": words[0].capitalize()
            }

        elif intent == "BUY_GRAIN":
            return {
                "buyer_name": words[0].capitalize()
            }

    return {}


def process_farmer_voice(message):

    # Handle empty messages
    if not message:
        return {
            "success": False,
            "message": "No voice message received"
        }

    # Get existing conversation
    conversation = get_conversation()

    # ----------------------------------------
    # CASE 1: NEW CONVERSATION
    # ----------------------------------------
    if not conversation:

        intent = detect_intent(message)

        extracted_entities = extract_entities(message)

        details = extracted_entities.copy()

        missing_fields = find_missing_information(
            intent,
            details
        )

        # Save incomplete request
        if missing_fields:

            start_conversation(
                intent,
                details
            )

            return {
                "success": False,
                "original_message": message,
                "detected_intent": intent,
                "details": details,
                "missing_information": missing_fields,
                "message": "Please provide: " +
                           ", ".join(missing_fields)
            }

        # Process complete request
        action_result = route_action(
            intent,
            details
        )

        return {
            "success": True,
            "original_message": message,
            "detected_intent": intent,
            "action": action_result["action"],
            "response": action_result["response"]
        }

    # ----------------------------------------
    # CASE 2: CONTINUE CONVERSATION
    # ----------------------------------------
    else:

        # Get saved intent and details
        intent = conversation["intent"]

        saved_details = conversation["details"].copy()

        # Extract information from the new message
        extracted_entities = extract_entities(message)

        # Extract possible name
        name_details = extract_name(
            message,
            intent
        )

        # Merge extracted details
        # ONLY replace values when the new value is not None
        for key, value in extracted_entities.items():

            if value is not None:
                saved_details[key] = value

        # Merge name details
        for key, value in name_details.items():

            if value is not None:
                saved_details[key] = value

        # Update conversation with merged details
        update_conversation(saved_details)

        # Get the final updated conversation
        conversation = get_conversation()

        details = conversation["details"]

        # Check missing information
        missing_fields = find_missing_information(
            intent,
            details
        )

        # If information is still missing
        if missing_fields:

            return {
                "success": False,
                "original_message": message,
                "detected_intent": intent,
                "details": details,
                "missing_information": missing_fields,
                "message": "Please provide: " +
                           ", ".join(missing_fields)
            }

        # All information is available
        action_result = route_action(
            intent,
            details
        )

        # Clear conversation after successful processing
        clear_conversation()

        return {
            "success": True,
            "original_message": message,
            "detected_intent": intent,
            "details": details,
            "action": action_result["action"],
            "response": action_result["response"]
        }


if __name__ == "__main__":

    messages = [
        "I want to sell rice",
        "500 kg from Bhimavaram",
        "Ramesh"
    ]

    for message in messages:

        print("Farmer:", message)

        result = process_farmer_voice(message)

        print("System:")
        print(result)

        print("-" * 60)