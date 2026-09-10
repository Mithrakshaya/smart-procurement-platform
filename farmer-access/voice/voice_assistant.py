import os
import sys


CURRENT_DIRECTORY = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIRECTORY = os.path.abspath(
    os.path.join(
        CURRENT_DIRECTORY,
        ".."
    )
)


sys.path.append(
    os.path.join(
        PROJECT_DIRECTORY,
        "ai"
    )
)

sys.path.append(
    os.path.join(
        PROJECT_DIRECTORY,
        "voice"
    )
)

sys.path.append(
    os.path.join(
        PROJECT_DIRECTORY,
        "conversation"
    )
)

sys.path.append(
    os.path.join(
        PROJECT_DIRECTORY,
        "actions"
    )
)


from speech_service import listen_to_farmer
from gemini_service import understand_farmer_message
from conversation_manager import ConversationManager
from action_router import route_action


conversation = ConversationManager()


def speak_response(message):

    try:

        import pyttsx3

        engine = pyttsx3.init()

        engine.say(message)

        engine.runAndWait()

    except Exception:

        print("Voice output is unavailable.")


def prepare_details(ai_result):

    details = {
        "grain_type": ai_result.get("commodity"),
        "quantity": ai_result.get("quantity"),
        "location": ai_result.get("location"),
        "request_id": ai_result.get("request_id")
    }

    person_name = ai_result.get("person_name")

    if person_name:

        if ai_result.get("intent") == "SELL_GRAIN":

            details["farmer_name"] = person_name

        elif ai_result.get("intent") == "BUY_GRAIN":

            details["buyer_name"] = person_name

    return details


def get_missing_information(intent, details):

    missing = []

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

    for field in required_fields:

        value = details.get(field)

        if value is None or value == "":
            missing.append(field)

    return missing


def create_missing_information_message(missing):

    readable_names = {
        "farmer_name": "your name",
        "buyer_name": "your name",
        "grain_type": "the product or commodity",
        "quantity": "the quantity",
        "location": "your location",
        "request_id": "your request ID"
    }

    readable_fields = []

    for field in missing:

        readable_fields.append(
            readable_names.get(
                field,
                field
            )
        )

    if len(readable_fields) == 1:

        return (
            "Please provide "
            + readable_fields[0]
            + "."
        )

    if len(readable_fields) == 2:

        return (
            "Please provide "
            + readable_fields[0]
            + " and "
            + readable_fields[1]
            + "."
        )

    return (
        "Please provide "
        + ", ".join(readable_fields[:-1])
        + ", and "
        + readable_fields[-1]
        + "."
    )


def process_farmer_message(message):

    current_conversation = conversation.get_conversation()

    previous_context = {}

    if current_conversation:

        previous_context = {
            "intent": current_conversation.get(
                "intent"
            ),
            "details": current_conversation.get(
                "details"
            )
        }

    ai_result = understand_farmer_message(
        message,
        previous_context
    )

    if ai_result.get("success") is False:

        error_message = (
            "Sorry, I am having trouble "
            "understanding your request right now."
        )

        return {
            "success": False,
            "message": error_message,
            "error": ai_result.get("error")
        }

    detected_intent = ai_result.get("intent")

    if detected_intent == "UNKNOWN":

        response_message = ai_result.get(
            "response"
        )

        if not response_message:

            response_message = (
                "Sorry, I could not understand "
                "your GrainFlow request."
            )

        return {
            "success": False,
            "original_message": message,
            "detected_intent": "UNKNOWN",
            "message": response_message
        }

    new_details = prepare_details(
        ai_result
    )

    existing_intent = conversation.get_intent()

    if existing_intent is None:

        conversation.start_conversation(
            detected_intent,
            new_details
        )

    else:

        if detected_intent == existing_intent:

            conversation.add_information(
                new_details
            )

        else:

            if detected_intent in [
                "SELL_GRAIN",
                "BUY_GRAIN",
                "CHECK_STATUS"
            ]:

                conversation.clear_conversation()

                conversation.start_conversation(
                    detected_intent,
                    new_details
                )

            else:

                conversation.add_information(
                    new_details
                )

    final_intent = conversation.get_intent()

    final_details = conversation.get_details()

    missing_information = get_missing_information(
        final_intent,
        final_details
    )

    if missing_information:

        response_message = create_missing_information_message(
            missing_information
        )

        return {
            "success": False,
            "original_message": message,
            "detected_intent": final_intent,
            "details": final_details,
            "missing_information": missing_information,
            "message": response_message
        }

    try:

        action_result = route_action(
            final_intent,
            final_details
        )

        conversation.clear_conversation()

        response_data = action_result.get(
            "response",
            {}
        )

        response_message = response_data.get(
            "message"
        )

        if not response_message:

            response_message = (
                "Your GrainFlow request "
                "has been processed successfully."
            )

        return {
            "success": True,
            "original_message": message,
            "detected_intent": final_intent,
            "details": final_details,
            "action": final_intent,
            "response": action_result,
            "message": response_message
        }

    except Exception as error:

        return {
            "success": False,
            "original_message": message,
            "detected_intent": final_intent,
            "details": final_details,
            "message": (
                "Sorry, there was a problem "
                "processing your request."
            ),
            "error": str(error)
        }


def run_voice_assistant():

    print()
    print("=" * 60)
    print("WELCOME TO GRAINFLOW VOICE ASSISTANT")
    print("=" * 60)

    welcome_message = (
        "Welcome to GrainFlow. "
        "You can tell me what you want to buy, "
        "sell, or track."
    )

    print()
    print("GRAINFLOW:", welcome_message)

    speak_response(
        welcome_message
    )

    while True:

        try:

            print()
            print(
                "Press Enter to START recording "
                "or type exit to stop."
            )

            user_choice = input()

            if user_choice.lower() == "exit":

                goodbye_message = (
                    "Thank you for using GrainFlow. "
                    "Goodbye."
                )

                print()
                print(
                    "GRAINFLOW:",
                    goodbye_message
                )

                speak_response(
                    goodbye_message
                )

                break

            voice_result = listen_to_farmer()

            if not voice_result.get("success"):

                error_message = (
                    "Sorry, I could not understand "
                    "your voice. Please try again."
                )

                print()
                print(
                    "GRAINFLOW:",
                    error_message
                )

                speak_response(
                    error_message
                )

                continue

            message = voice_result.get(
                "message"
            )

            if not message:

                continue

            print()
            print(
                "Processing your request..."
            )

            result = process_farmer_message(
                message
            )

            print()
            print(
                "GRAINFLOW RESPONSE:"
            )

            print(
                result
            )

            response_message = result.get(
                "message"
            )

            if response_message:

                print()
                print(
                    "GRAINFLOW:",
                    response_message
                )

                speak_response(
                    response_message
                )

        except KeyboardInterrupt:

            print()
            print(
                "Voice assistant stopped."
            )

            break

        except Exception as error:

            print()
            print(
                "Error:",
                error
            )


if __name__ == "__main__":

    run_voice_assistant()