import sys
import os

# Get the path of the Grain folder
grain_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "grain")
)

# Add Grain folder to Python path
sys.path.append(grain_path)

# Import Sell Grain function
from sell_grain import create_sell_request


def route_action(intent, farmer_details=None):

    # Handle SELL_GRAIN request
    if intent == "SELL_GRAIN":

        # Check whether farmer details are available
        if not farmer_details:
            return {
                "action": "SELL_GRAIN",
                "response": "Please provide farmer details to create a selling request"
            }

        # Create the actual selling request
        result = create_sell_request(
            farmer_name=farmer_details.get("farmer_name"),
            grain_type=farmer_details.get("grain_type"),
            quantity=farmer_details.get("quantity", 0),
            location=farmer_details.get("location")
        )

        return {
            "action": "SELL_GRAIN",
            "response": result
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

    farmer_details = {
        "farmer_name": "Ramesh",
        "grain_type": "Rice",
        "quantity": 500,
        "location": "Bhimavaram"
    }

    result = route_action("SELL_GRAIN", farmer_details)

    print(result)