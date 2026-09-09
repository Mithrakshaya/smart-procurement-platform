from pydantic import BaseModel
from datetime import date

class BookingCreate(BaseModel):
    farmer_name: str
    crop: str
    quantity: float
    booking_date: date
    
class BookingReschedule(BaseModel):
    booking_id: int
    new_booking_date: date