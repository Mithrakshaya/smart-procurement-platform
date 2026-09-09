from .schemas import BookingCreate, BookingReschedule

from datetime import timedelta

bookings = []
booking_counter = 1

MAX_CAPACITY = 5


def create_booking(data: BookingCreate):
    global booking_counter

    count = sum(
        1 for booking in bookings
        if booking["booking_date"] == data.booking_date
    )

    if count >= MAX_CAPACITY:
        return {
            "message": "Slot Full",
            "booking_date": data.booking_date,
            "capacity": MAX_CAPACITY
        }

    booking = {
        "booking_id": booking_counter,
        "confirmation_token": f"GF-{booking_counter:04d}",
        "farmer_name": data.farmer_name,
        "crop": data.crop,
        "quantity": data.quantity,
        "booking_date": data.booking_date,
        "status": "Confirmed"
    }

    bookings.append(booking)
    booking_counter += 1

    return booking

def reschedule_booking(data: BookingReschedule):
    for booking in bookings:
        if booking["booking_id"] == data.booking_id:

            count = sum(
                1 for b in bookings
                if b["booking_date"] == data.new_booking_date
            )

            if count >= MAX_CAPACITY:
                return {
                    "message": "New slot is full",
                    "booking_date": data.new_booking_date,
                    "capacity": MAX_CAPACITY
                }

            booking["booking_date"] = data.new_booking_date
            return booking

    return {"message": "Booking not found"}

def suggest_alternative_slots(requested_date):
    suggestions = []

    for i in range(1, 4):
        new_date = requested_date + __import__("datetime").timedelta(days=i)

        count = sum(
            1 for booking in bookings
            if booking["booking_date"] == new_date
        )

        if count < MAX_CAPACITY:
            suggestions.append({
                "date": new_date,
                "available_slots": MAX_CAPACITY - count
            })

    return suggestions

def get_bookings():
    return bookings