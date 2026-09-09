from fastapi import APIRouter
from datetime import date
from .schemas import BookingCreate, BookingReschedule
from .service import create_booking, get_bookings, reschedule_booking, suggest_alternative_slots

router = APIRouter(
    prefix="/booking",
    tags=["Smart Booking"]
)

@router.post("/")
def add_booking(data: BookingCreate):
    return create_booking(data)

@router.put("/reschedule")
def reschedule(data: BookingReschedule):
    return reschedule_booking(data)

@router.get("/")
def list_bookings():
    return get_bookings()

@router.get("/alternatives")
def alternatives(requested_date: date):
    return suggest_alternative_slots(requested_date)