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


def process_farmer_voice(message):

    if not message:
        return {
            "success": False,
            "message": "No voice message received"
        }

    # Step 1: Detect farmer intent
    intent = detect_intent(message)

    # Step 2: Route the detected intent to the correct action
    action_result = route_action(intent)

    return {
        "success": True,
        "original_message": message,
        "detected_intent": intent,
        "action": action_result["action"],
        "response": action_result["response"]
    }


if __name__ == "__main__":

    test_messages = [
        "I want to sell my rice",
        "I want to buy wheat",
        "I want to track my order",
        "Hello, I need help"
    ]

    for message in test_messages:
        result = process_farmer_voice(message)
        print(result)