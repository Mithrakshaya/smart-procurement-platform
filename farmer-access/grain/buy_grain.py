def create_buy_request(buyer_name, grain_type, quantity, location):

    # Validate buyer name
    if not buyer_name:
        return {
            "success": False,
            "message": "Buyer name is required"
        }

    # Validate grain type
    if not grain_type:
        return {
            "success": False,
            "message": "Grain type is required"
        }

    # Validate quantity
    if quantity <= 0:
        return {
            "success": False,
            "message": "Quantity must be greater than zero"
        }

    # Validate location
    if not location:
        return {
            "success": False,
            "message": "Location is required"
        }

    # Create the grain buying request
    buy_request = {
        "buyer_name": buyer_name,
        "grain_type": grain_type,
        "quantity": quantity,
        "location": location,
        "status": "REQUEST_CREATED"
    }

    return {
        "success": True,
        "message": "Grain buying request created successfully",
        "request": buy_request
    }


if __name__ == "__main__":

    result = create_buy_request(
        buyer_name="Suresh",
        grain_type="Wheat",
        quantity=300,
        location="Bhimavaram"
    )

    print(result)