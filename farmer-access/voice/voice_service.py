import sys
import os


# Get the main farmer-access folder path
base_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# Get NLP and Actions folder paths
nlp_path = os.path.join(base_path, "nlp")
actions_path = os.path.join(base_path, "actions")

# Add folders to Python path
sys.path.append(nlp_path)
sys.path.append(actions_path)


# Import required modules
from intent_detector import detect_intent
from entity_extractor import extract_entities
from missing_info_detector import find_missing_information
from action_router import route_action


def process_farmer_voice(message, farmer_details=None):

    # Check whether a message was received
    if not message:
        return {
            "success": False,
            "message": "No voice message received"
        }

    # Step 1: Detect the farmer's intent
    intent = detect_intent(message)

    # Step 2: Extract information from the message
    extracted_entities = extract_entities(message)

    # Step 3: Start with automatically extracted details
    final_details = extracted_entities.copy()

    # Step 4: Add manually provided details
    if farmer_details:
        final_details.update(farmer_details)

    # Step 5: Check for missing required information
    missing_fields = find_missing_information(
        intent,
        final_details
    )

    # Step 6: Stop if required information is missing
    if missing_fields:
        return {
            "success": False,
            "original_message": message,
            "detected_intent": intent,
            "extracted_entities": extracted_entities,
            "final_details": final_details,
            "missing_information": missing_fields,
            "message": "Please provide: " + ", ".join(missing_fields)
        }

    # Step 7: Route the request to the correct workflow
    action_result = route_action(
        intent,
        final_details
    )

    # Step 8: Return the complete result
    return {
        "success": True,
        "original_message": message,
        "detected_intent": intent,
        "extracted_entities": extracted_entities,
        "final_details": final_details,
        "action": action_result["action"],
        "response": action_result["response"]
    }


if __name__ == "__main__":

    # TEST 1: Complete SELL_GRAIN request
    print("TEST 1: COMPLETE SELL_GRAIN")

    result = process_farmer_voice(
        "I want to sell 500 kg of rice from Bhimavaram",
        {
            "farmer_name": "Ramesh"
        }
    )

    print(result)
    print()


    # TEST 2: Missing information in SELL_GRAIN
    print("TEST 2: MISSING INFORMATION")

    result = process_farmer_voice(
        "I want to sell rice"
    )

    print(result)
    print()


    # TEST 3: Complete BUY_GRAIN request
    print("TEST 3: COMPLETE BUY_GRAIN")

    result = process_farmer_voice(
        "I want to buy 300 kg of wheat in Hyderabad",
        {
            "buyer_name": "Suresh"
        }
    )

    print(result)
    print()


    # TEST 4: CHECK_STATUS with request ID
    print("TEST 4: CHECK_STATUS")

    result = process_farmer_voice(
        "What is the status of request REQ002?"
    )

    print(result)