import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "nlp")
    )
)

from intent_detector import detect_intent


def test_sell_grain():
    result = detect_intent("I want to sell my rice")
    assert result == "SELL_GRAIN"


def test_buy_grain():
    result = detect_intent("I want to buy wheat")
    assert result == "BUY_GRAIN"


def test_check_status():
    result = detect_intent("I want to track my order")
    assert result == "CHECK_STATUS"


def test_unknown_request():
    result = detect_intent("Hello, I need some help")
    assert result == "UNKNOWN"


if __name__ == "__main__":
    test_sell_grain()
    test_buy_grain()
    test_check_status()
    test_unknown_request()

    print("All intent detection tests passed successfully")