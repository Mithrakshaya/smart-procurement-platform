import sys
import os

# Get the paths of the NLP and Actions folders
base_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

nlp_path = os.path.join(base_path, "nlp")
actions_path = os.path.join(base_path, "actions")

# Add folders to Python path
sys.path.append(nlp_path)
sys.path.append(actions_path)

# Import modules
from intent_detector import detect_intent
from action_router import route_action


def process_farmer_voice(message, farmer_details=None):

    if not message:
        return {
            "success": False,
            "message": "No voice message received"
        }

    # Step 1: Detect farmer intent
    intent = detect_intent(message)

    # Step 2: Send intent and farmer details to Action Router
    action_result = route_action(intent, farmer_details)

    return {
        "success": True,
        "original_message": message,
        "detected_intent": intent,
        "action": action_result["action"],
        "response": action_result["response"]
    }


if __name__ == "__main__":

    # Farmer details for testing the Sell Grain workflow
    farmer_details = {
        "farmer_name": "Ramesh",
        "grain_type": "Rice",
        "quantity": 500,
        "location": "Bhimavaram"
    }

    # Test SELL_GRAIN with actual farmer details
    result = process_farmer_voice(
        "I want to sell my rice",
        farmer_details
    )

    print(result)