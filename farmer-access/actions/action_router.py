import sys
import os

# Get the base path of farmer-access
base_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# Get paths of required folders
grain_path = os.path.join(base_path, "grain")
status_path = os.path.join(base_path, "status")

# Add folders to Python path
sys.path.append(grain_path)
sys.path.append(status_path)

# Import Grain workflow functions
from sell_grain import create_sell_request
from buy_grain import create_buy_request

# Import Status workflow function
from status_service import check_request_status


def route_action(intent, farmer_details=None):

    # Handle SELL_GRAIN request
    if intent == "SELL_GRAIN":

        if not farmer_details:
            return {
                "action": "SELL_GRAIN",
                "response": "Please provide farmer details to create a selling request"
            }

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

    # Handle BUY_GRAIN request
    elif intent == "BUY_GRAIN":

        if not farmer_details:
            return {
                "action": "BUY_GRAIN",
                "response": "Please provide buyer details to create a buying request"
            }

        result = create_buy_request(
            buyer_name=farmer_details.get("buyer_name"),
            grain_type=farmer_details.get("grain_type"),
            quantity=farmer_details.get("quantity", 0),
            location=farmer_details.get("location")
        )

        return {
            "action": "BUY_GRAIN",
            "response": result
        }

    # Handle CHECK_STATUS request
    elif intent == "CHECK_STATUS":

        if not farmer_details:
            return {
                "action": "CHECK_STATUS",
                "response": "Please provide a request ID to check the status"
            }

        request_id = farmer_details.get("request_id")

        result = check_request_status(request_id)

        return {
            "action": "CHECK_STATUS",
            "response": result
        }

    # Handle unknown requests
    else:
        return {
            "action": "UNKNOWN",
            "response": "Sorry, I could not understand your request"
        }


if __name__ == "__main__":

    # Test SELL_GRAIN
    seller_details = {
        "farmer_name": "Ramesh",
        "grain_type": "Rice",
        "quantity": 500,
        "location": "Bhimavaram"
    }

    sell_result = route_action("SELL_GRAIN", seller_details)
    print("SELL_GRAIN →", sell_result)

    # Test BUY_GRAIN
    buyer_details = {
        "buyer_name": "Suresh",
        "grain_type": "Wheat",
        "quantity": 300,
        "location": "Bhimavaram"
    }

    buy_result = route_action("BUY_GRAIN", buyer_details)
    print("BUY_GRAIN →", buy_result)

    # Test CHECK_STATUS
    status_details = {
        "request_id": "REQ002"
    }

    status_result = route_action("CHECK_STATUS", status_details)
    print("CHECK_STATUS →", status_result)