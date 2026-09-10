from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from backend.app.db.database import SessionLocal
from backend.app.modules.farmer.model import Farmer
from backend.app.modules.booking.service import bookings

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dashboard Summary
@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db)
):
    today = date.today()

    farmers = db.query(Farmer).all()

    todays_farmers = len(farmers)

    upcoming_appointments = sum(
        1 for booking in bookings
        if booking["booking_date"] >= today
    )

    current_queue = len(bookings)

    average_waiting_time = current_queue * 5

    expected_arrivals = upcoming_appointments

    if current_queue >= 30:
        congestion_level = "High"
    elif current_queue >= 15:
        congestion_level = "Medium"
    else:
        congestion_level = "Low"

    daily_target = sum(
        farmer.quantity for farmer in farmers
    )

    procured = sum(
        farmer.quantity
        for farmer in farmers
        if farmer.status.lower() == "completed"
    )

    remaining = max(daily_target - procured, 0)

    return {
        "todays_farmers": todays_farmers,
        "upcoming_appointments": upcoming_appointments,
        "current_queue": current_queue,
        "average_waiting_time": average_waiting_time,
        "expected_arrivals": expected_arrivals,
        "congestion_level": congestion_level,
        "daily_target": daily_target,
        "procured": procured,
        "remaining": remaining
    }


# Centre-wise Performance
@router.get("/centres")
def get_centre_performance(
    db: Session = Depends(get_db)
):
    farmers = db.query(Farmer).all()

    centres = {}

    for farmer in farmers:
        centre = farmer.location

        if centre not in centres:
            centres[centre] = {
                "farmers": 0,
                "procurement": 0
            }

        centres[centre]["farmers"] += 1
        centres[centre]["procurement"] += farmer.quantity

    result = []

    for centre, data in centres.items():

        if data["farmers"] >= 30:
            status = "Busy"
        elif data["farmers"] >= 15:
            status = "Active"
        else:
            status = "Normal"

        result.append({
            "centre": centre,
            "farmers": data["farmers"],
            "queue": 0,
            "procurement": data["procurement"],
            "status": status
        })

    return result


# System Alerts
@router.get("/alerts")
def get_dashboard_alerts(
    db: Session = Depends(get_db)
):
    farmers = db.query(Farmer).all()

    alerts = []

    if len(farmers) > 30:
        alerts.append({
            "type": "warning",
            "title": "High Farmer Load",
            "message": f"{len(farmers)} farmers are currently registered."
        })

    upcoming = sum(
        1 for booking in bookings
        if booking["booking_date"] >= date.today()
    )

    if upcoming > 10:
        alerts.append({
            "type": "warning",
            "title": "High Appointment Load",
            "message": f"{upcoming} upcoming appointments detected."
        })

    if not alerts:
        alerts.append({
            "type": "info",
            "title": "System Status",
            "message": "No major alerts at the moment."
        })

    return alerts