from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# Dashboard Summary
@router.get("/summary")
def get_dashboard_summary():
    return {
        "todays_farmers": 120,
        "upcoming_appointments": 35,
        "current_queue": 18,
        "average_waiting_time": 25,
        "expected_arrivals": 42,
        "congestion_level": "Medium",
        "daily_target": 1000,
        "procured": 720,
        "remaining": 280
    }


# Centre-wise Performance
@router.get("/centres")
def get_centre_performance():
    return [
        {
            "centre": "Bhimavaram Centre",
            "farmers": 120,
            "queue": 18,
            "procurement": 720,
            "status": "Active"
        },
        {
            "centre": "Tanuku Centre",
            "farmers": 105,
            "queue": 12,
            "procurement": 650,
            "status": "Normal"
        },
        {
            "centre": "Palakollu Centre",
            "farmers": 145,
            "queue": 31,
            "procurement": 810,
            "status": "Busy"
        },
        {
            "centre": "Narasapur Centre",
            "farmers": 98,
            "queue": 9,
            "procurement": 590,
            "status": "Normal"
        }
    ]
# System Alerts
@router.get("/alerts")
def get_dashboard_alerts():
    return [
        {
            "type": "warning",
            "title": "Palakollu Centre",
            "message": "High queue detected. Consider increasing counter capacity."
        },
        {
            "type": "ai",
            "title": "AI Recommendation",
            "message": "Expected farmer arrivals may increase during peak hours. Allocate additional staff to high-load centres."
        }
    ]