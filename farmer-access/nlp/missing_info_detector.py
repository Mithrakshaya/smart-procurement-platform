def find_missing_information(intent, details):

    if intent == "SELL_GRAIN":
        required_fields = [
            "farmer_name",
            "grain_type",
            "quantity",
            "location"
        ]

    elif intent == "BUY_GRAIN":
        required_fields = [
            "buyer_name",
            "grain_type",
            "quantity",
            "location"
        ]

    elif intent == "CHECK_STATUS":
        required_fields = [
            "request_id"
        ]

    else:
        return []

    missing_fields = []

    for field in required_fields:
        if not details.get(field):
            missing_fields.append(field)

    return missing_fields


if __name__ == "__main__":

    seller_details = {
        "farmer_name": "Ramesh",
        "grain_type": "Rice",
        "quantity": None,
        "location": None
    }

    result = find_missing_information(
        "SELL_GRAIN",
        seller_details
    )

    print("SELL_GRAIN Missing Information:")
    print(result)
    print()

    buyer_details = {
        "buyer_name": None,
        "grain_type": "Wheat",
        "quantity": 300,
        "location": "Hyderabad"
    }

    result = find_missing_information(
        "BUY_GRAIN",
        buyer_details
    )

    print("BUY_GRAIN Missing Information:")
    print(result)
    print()

    status_details = {
        "request_id": None
    }

    result = find_missing_information(
        "CHECK_STATUS",
        status_details
    )

    print("CHECK_STATUS Missing Information:")
    print(result)