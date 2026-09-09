import sys
import os


# ==========================================
# GET REQUIRED FOLDER PATHS
# ==========================================

base_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

nlp_path = os.path.join(base_path, "nlp")
actions_path = os.path.join(base_path, "actions")


# ==========================================
# ADD PATHS TO PYTHON PATH
# ==========================================

sys.path.append(nlp_path)
sys.path.append(actions_path)


# ==========================================
# IMPORT REQUIRED MODULES
# ==========================================

from intent_detector import detect_intent
from entity_extractor import extract_entities
from action_router import route_action


# ==========================================
# PROCESS FARMER MESSAGE
# ==========================================

def process_farmer_voice(message, farmer_details=None):

    # Check whether a message was received
    if not message:
        return {
            "success": False,
            "message": "No voice message received"
        }

    # Step 1: Detect intent
    intent = detect_intent(message)

    # Step 2: Extract entities automatically
    extracted_entities = extract_entities(message)

    # Step 3: Start with automatically extracted entities
    final_details = extracted_entities.copy()

    # Step 4: Add manually provided details if available
    if farmer_details:
        final_details.update(farmer_details)

    # Step 5: Send intent and details to Action Router
    action_result = route_action(
        intent,
        final_details
    )

    # Step 6: Return complete result
    return {
        "success": True,
        "original_message": message,
        "detected_intent": intent,
        "extracted_entities": extracted_entities,
        "final_details": final_details,
        "action": action_result["action"],
        "response": action_result["response"]
    }


# ==========================================
# TEST COMPLETE FARMER WORKFLOW
# ==========================================

if __name__ == "__main__":

    # ------------------------------------------
    # TEST 1: SELL GRAIN
    # ------------------------------------------

    sell_result = process_farmer_voice(
        "I want to sell 500 kg of rice from Bhimavaram",
        {
            "farmer_name": "Ramesh"
        }
    )

    print("SELL_GRAIN")
    print(sell_result)
    print()


    # ------------------------------------------
    # TEST 2: BUY GRAIN
    # ------------------------------------------

    buy_result = process_farmer_voice(
        "I want to buy 300 kg of wheat in Hyderabad",
        {
            "buyer_name": "Suresh"
        }
    )

    print("BUY_GRAIN")
    print(buy_result)
    print()


    # ------------------------------------------
    # TEST 3: CHECK STATUS AUTOMATICALLY
    # ------------------------------------------

    status_result = process_farmer_voice(
        "What is the status of request REQ002?"
    )

    print("CHECK_STATUS")
    print(status_result)