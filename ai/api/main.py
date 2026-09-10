from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

import sys
from pathlib import Path

# Add prediction folder to Python path
PREDICTION_DIR = Path(__file__).resolve().parents[1] / "prediction"
sys.path.append(str(PREDICTION_DIR))

from predict_arrivals import predict_arrivals
from predict_queue import predict_queue
from predict_waiting_time import predict_waiting_time
from predict_congestion import predict_congestion, get_congestion_level


# --------------------------------------------------
# CREATE FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="GrainFlow AI Prediction API",
    description="AI Prediction and Queue Management API",
    version="1.0.0"
)


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "GrainFlow AI API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# GENERIC FEATURE INPUT
# --------------------------------------------------

class PredictionRequest(BaseModel):

    day_of_week: float
    centre_id: float
    time_slot: float
    total_slots: float
    booked_slots: float
    farmers_arrived: float
    average_procurement_time: float
    crop_type: float
    quantity: float
    weather: float
    temperature: float
    rainfall: float
    harvest_season: float
    holiday: float
    previous_day_arrivals: float
    previous_slot_arrivals: float
    year: float
    month: float
    day: float
    booking_ratio: float
    queue_per_slot: float
    arrival_pressure: float
    procurement_load: float
    historical_arrival_trend: float
    weather_impact: float
    queue_pressure: float


# --------------------------------------------------
# FARMER ARRIVAL API
# --------------------------------------------------

@app.post("/predict/arrivals")
def predict_farmer_arrivals(request: PredictionRequest):

    try:

        data = pd.DataFrame(
            [request.model_dump()]
        )

        prediction = predict_arrivals(data)[0]

        return {
            "prediction_type": "farmer_arrivals",
            "predicted_arrivals": round(
                float(prediction),
                2
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# QUEUE API
# --------------------------------------------------

@app.post("/predict/queue")
def predict_queue_length(request: PredictionRequest):

    try:

        data = pd.DataFrame(
            [request.model_dump()]
        )

        prediction = predict_queue(data)[0]

        return {
            "prediction_type": "queue_length",
            "predicted_queue": round(
                float(prediction),
                2
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# WAITING TIME API
# --------------------------------------------------

@app.post("/predict/waiting-time")
def predict_waiting(request: PredictionRequest):

    try:

        data = pd.DataFrame(
            [request.model_dump()]
        )

        prediction = predict_waiting_time(data)[0]

        return {
            "prediction_type": "waiting_time",
            "predicted_waiting_time": round(
                float(prediction),
                2
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# CONGESTION API
# --------------------------------------------------

@app.post("/predict/congestion")
def predict_centre_congestion(
    request: PredictionRequest
):

    try:

        data = pd.DataFrame(
            [request.model_dump()]
        )

        prediction = predict_congestion(data)[0]

        level = get_congestion_level(
            prediction
        )

        return {
            "prediction_type": "congestion",
            "congestion_score": round(
                float(prediction),
                2
            ),
            "congestion_level": level
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )