import sys
import os

# Get the path of the NLP folder
nlp_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "nlp")
)

# Add NLP folder to Python path
sys.path.append(nlp_path)

# Import intent detection function
from intent_detector import detect_intent


def process_farmer_voice(message):

    if not message:
        return {
            "success": False,
            "message": "No voice message received"
        }

    # Detect the farmer's intention
    intent = detect_intent(message)

    return {
        "success": True,
        "original_message": message,
        "detected_intent": intent,
        "message": "Farmer request processed successfully"
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
        