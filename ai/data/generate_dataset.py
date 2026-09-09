# ============================================================
# GRAINFLOW HISTORICAL DATASET GENERATOR
# Member 3 - AI Prediction & Queue Management
# ============================================================

import os
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

np.random.seed(42)

NUM_DAYS = 200
NUM_CENTRES = 5
NUM_TIME_SLOTS = 8

START_DATE = "2025-01-01"

OUTPUT_PATH = os.path.join(
    "ai",
    "data",
    "grainflow_historical_data.csv"
)


# ============================================================
# MASTER SETTINGS
# ============================================================

CENTRES = {
    "Centre_1": {
        "capacity": 50,
        "factor": 0.90
    },
    "Centre_2": {
        "capacity": 45,
        "factor": 1.00
    },
    "Centre_3": {
        "capacity": 60,
        "factor": 1.15
    },
    "Centre_4": {
        "capacity": 40,
        "factor": 0.85
    },
    "Centre_5": {
        "capacity": 55,
        "factor": 1.05
    }
}


TIME_SLOTS = [
    "06:00-08:00",
    "08:00-10:00",
    "10:00-12:00",
    "12:00-14:00",
    "14:00-16:00",
    "16:00-18:00",
    "18:00-20:00",
    "20:00-22:00"
]


SLOT_DEMAND = {
    "06:00-08:00": 0.75,
    "08:00-10:00": 1.00,
    "10:00-12:00": 1.20,
    "12:00-14:00": 0.90,
    "14:00-16:00": 1.05,
    "16:00-18:00": 1.25,
    "18:00-20:00": 1.10,
    "20:00-22:00": 0.70
}


CROP_TYPES = [
    "Rice",
    "Wheat",
    "Maize",
    "Cotton",
    "Groundnut"
]


CROP_FACTOR = {
    "Rice": 1.10,
    "Wheat": 0.90,
    "Maize": 1.00,
    "Cotton": 1.20,
    "Groundnut": 0.95
}


WEATHER_TYPES = [
    "Sunny",
    "Cloudy",
    "Rainy"
]


SEASONS = [
    "Normal",
    "Harvest"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_season(month):
    """
    Determine agricultural season.
    """

    if month in [10, 11, 12, 1, 2]:
        return "Harvest"

    return "Normal"


def get_weather():
    """
    Generate realistic weather.
    """

    value = np.random.rand()

    if value < 0.60:
        return "Sunny"

    elif value < 0.85:
        return "Cloudy"

    else:
        return "Rainy"


def get_weather_effect(weather):
    """
    Effect of weather on farmer arrivals.
    """

    if weather == "Sunny":
        return 1.00

    elif weather == "Cloudy":
        return 0.95

    else:
        return 0.75


def get_temperature(weather, month):
    """
    Generate temperature based on weather and month.
    """

    if month in [12, 1, 2]:
        base = 24
    elif month in [3, 4, 5]:
        base = 32
    elif month in [6, 7, 8, 9]:
        base = 29
    else:
        base = 27

    if weather == "Sunny":
        return round(np.random.normal(base + 2, 2), 2)

    elif weather == "Cloudy":
        return round(np.random.normal(base, 2), 2)

    else:
        return round(np.random.normal(base - 2, 2), 2)


def get_rainfall(weather):
    """
    Generate rainfall based on weather.
    """

    if weather == "Sunny":
        return round(max(0, np.random.normal(1, 1)), 2)

    elif weather == "Cloudy":
        return round(max(0, np.random.normal(5, 3)), 2)

    else:
        return round(max(5, np.random.normal(25, 10)), 2)


def get_holiday():
    """
    Small probability of holiday.
    """

    return 1 if np.random.rand() < 0.05 else 0


def get_crop():
    """
    Select crop type.
    """

    probabilities = [
        0.35,
        0.15,
        0.20,
        0.15,
        0.15
    ]

    return np.random.choice(
        CROP_TYPES,
        p=probabilities
    )


# ============================================================
# GENERATE DATA
# ============================================================

records = []


dates = pd.date_range(
    start=START_DATE,
    periods=NUM_DAYS,
    freq="D"
)


# Store previous-day arrivals for each centre
previous_day_values = {
    centre: 70
    for centre in CENTRES
}


# Store previous-slot arrivals
previous_slot_values = {
    centre: 70
    for centre in CENTRES
}


# ============================================================
# MAIN LOOP
# ============================================================

for date in dates:

    day_name = date.day_name()
    month = date.month

    # Weekend effect
    if day_name in ["Saturday", "Sunday"]:
        day_factor = 0.85
    else:
        day_factor = 1.00

    season = get_season(month)

    if season == "Harvest":
        season_factor = 1.25
    else:
        season_factor = 0.90

    holiday = get_holiday()

    if holiday == 1:
        holiday_factor = 0.65
    else:
        holiday_factor = 1.00


    # --------------------------------------------------------
    # Generate each centre
    # --------------------------------------------------------

    for centre_name, centre_info in CENTRES.items():

        capacity = centre_info["capacity"]
        centre_factor = centre_info["factor"]

        previous_day_arrivals = previous_day_values[
            centre_name
        ]

        previous_slot_arrivals = previous_slot_values[
            centre_name
        ]


        # ----------------------------------------------------
        # Generate all slots for this centre/day
        # ----------------------------------------------------

        daily_records = []


        for slot_index, time_slot in enumerate(TIME_SLOTS):

            slot_factor = SLOT_DEMAND[time_slot]

            weather = get_weather()

            weather_factor = get_weather_effect(
                weather
            )

            temperature = get_temperature(
                weather,
                month
            )

            rainfall = get_rainfall(
                weather
            )

            crop_type = get_crop()

            crop_factor = CROP_FACTOR[
                crop_type
            ]


            # ------------------------------------------------
            # Current farmer arrivals
            # ------------------------------------------------

            base_arrivals = (
                75
                * day_factor
                * season_factor
                * holiday_factor
                * slot_factor
                * centre_factor
                * weather_factor
                * crop_factor
            )


            # Historical influence
            historical_effect = (
                0.15 * previous_day_arrivals
                + 0.20 * previous_slot_arrivals
            )


            arrivals = (
                0.65 * base_arrivals
                + historical_effect
                + np.random.normal(0, 7)
            )


            farmers_arrived = int(
                max(
                    8,
                    round(arrivals)
                )
            )


            # ------------------------------------------------
            # Bookings
            # ------------------------------------------------

            booking_probability = np.random.uniform(
                0.55,
                0.85
            )

            booked_slots = int(
                max(
                    0,
                    min(
                        farmers_arrived,
                        round(
                            farmers_arrived
                            * booking_probability
                        )
                    )
                )
            )


            # ------------------------------------------------
            # Procurement time
            # ------------------------------------------------

            base_procurement_time = {
                "Rice": 14,
                "Wheat": 11,
                "Maize": 12,
                "Cotton": 18,
                "Groundnut": 10
            }[crop_type]


            average_procurement_time = (
                base_procurement_time
                + np.random.normal(0, 2)
            )

            average_procurement_time = round(
                max(
                    5,
                    average_procurement_time
                ),
                2
            )


            # ------------------------------------------------
            # Current queue
            # ------------------------------------------------

            service_capacity = (
                capacity
                * (60 / average_procurement_time)
                * 0.12
            )


            current_queue = (
                max(
                    0,
                    previous_slot_arrivals
                    - service_capacity
                )
            )


            queue_noise = np.random.normal(
                0,
                5
            )


            queue_length = int(
                max(
                    0,
                    round(
                        current_queue
                        + queue_noise
                    )
                )
            )


            # ------------------------------------------------
            # Current waiting time
            # ------------------------------------------------

            average_waiting_time = (
                queue_length
                * average_procurement_time
                / max(
                    service_capacity,
                    1
                )
            )


            average_waiting_time += np.random.normal(
                0,
                4
            )


            average_waiting_time = round(
                max(
                    2,
                    average_waiting_time
                ),
                2
            )


            # ------------------------------------------------
            # Quantity
            # ------------------------------------------------

            quantity = (
                farmers_arrived
                * np.random.uniform(
                    0.8,
                    2.5
                )
            )

            quantity = round(
                max(
                    10,
                    quantity
                ),
                2
            )


            # ------------------------------------------------
            # Store current record
            # ------------------------------------------------

            daily_records.append({
                "date": date.strftime("%Y-%m-%d"),
                "day_of_week": day_name,
                "centre_id": centre_name,
                "time_slot": time_slot,
                "total_slots": capacity,
                "booked_slots": booked_slots,
                "farmers_arrived": farmers_arrived,
                "queue_length": queue_length,
                "average_waiting_time": average_waiting_time,
                "average_procurement_time":
                    average_procurement_time,
                "crop_type": crop_type,
                "quantity": quantity,
                "weather": weather,
                "temperature": temperature,
                "rainfall": rainfall,
                "harvest_season": season,
                "holiday": holiday,
                "previous_day_arrivals":
                    int(previous_day_arrivals),
                "previous_slot_arrivals":
                    int(previous_slot_arrivals)
            })


            # Update previous slot
            previous_slot_arrivals = farmers_arrived


        # ====================================================
        # CREATE NEXT-SLOT TARGETS
        # ====================================================

        for i in range(len(daily_records) - 1):

            current_record = daily_records[i]

            next_record = daily_records[i + 1]


            # ------------------------------------------------
            # Target arrivals
            # ------------------------------------------------

            target_arrivals = (
                next_record["farmers_arrived"]
                + np.random.normal(0, 2)
            )

            target_arrivals = round(
                max(
                    1,
                    target_arrivals
                ),
                2
            )


            # ------------------------------------------------
            # Target queue
            # ------------------------------------------------

            future_capacity = (
                next_record["total_slots"]
                * (
                    60
                    / next_record[
                        "average_procurement_time"
                    ]
                )
                * 0.12
            )


            arrival_pressure = (
                target_arrivals
                / max(
                    next_record["total_slots"],
                    1
                )
            )


            booking_pressure = (
                next_record["booked_slots"]
                / max(
                    next_record["total_slots"],
                    1
                )
            )


            # Queue is influenced by future arrivals,
            # bookings and previous-slot conditions.
            target_queue = (
                target_arrivals
                * 0.45
                + booking_pressure
                * next_record["total_slots"]
                * 0.35
                + next_record[
                    "previous_slot_arrivals"
                ]
                * 0.20
                - future_capacity
                * 0.25
                + np.random.normal(0, 5)
            )


            # Keep queue within realistic bounds
            target_queue = round(
                max(
                    0,
                    min(
                        120,
                        target_queue
                    )
                ),
                2
            )


            # ------------------------------------------------
            # Target waiting time
            # ------------------------------------------------

            target_waiting_time = (
                target_queue
                * next_record[
                    "average_procurement_time"
                ]
                / max(
                    future_capacity,
                    1
                )
            )


            # Additional effects
            target_waiting_time += (
                arrival_pressure * 10
            )

            target_waiting_time += np.random.normal(
                0,
                5
            )


            target_waiting_time = round(
                max(
                    2,
                    min(
                        180,
                        target_waiting_time
                    )
                ),
                2
            )


            # ------------------------------------------------
            # Congestion score
            # ------------------------------------------------

            capacity_ratio = (
                target_arrivals
                / max(
                    next_record["total_slots"],
                    1
                )
            )


            queue_ratio = (
                target_queue
                / max(
                    next_record["total_slots"],
                    1
                )
            )


            booking_ratio = (
                next_record["booked_slots"]
                / max(
                    next_record["total_slots"],
                    1
                )
            )


            waiting_ratio = (
                target_waiting_time
                / 120
            )


            congestion_score = (
                100
                * (
                    0.35 * capacity_ratio
                    + 0.25 * queue_ratio
                    + 0.20 * booking_ratio
                    + 0.20 * waiting_ratio
                )
            )


            # Small random variation
            congestion_score += np.random.normal(
                0,
                4
            )


            congestion_score = round(
                max(
                    0,
                    min(
                        100,
                        congestion_score
                    )
                ),
                2
            )


            # ------------------------------------------------
            # Congestion category
            # ------------------------------------------------

            if congestion_score < 35:
                congestion_level = "LOW"

            elif congestion_score < 65:
                congestion_level = "MEDIUM"

            else:
                congestion_level = "HIGH"


            # ------------------------------------------------
            # Add targets to current record
            # ------------------------------------------------

            current_record["target_arrivals"] = (
                target_arrivals
            )

            current_record["target_queue_length"] = (
                target_queue
            )

            current_record["target_waiting_time"] = (
                target_waiting_time
            )

            current_record["target_congestion_score"] = (
                congestion_score
            )

            current_record["target_congestion_level"] = (
                congestion_level
            )


            records.append(current_record)


        # ----------------------------------------------------
        # Update daily history
        # ----------------------------------------------------

        previous_day_values[
            centre_name
        ] = daily_records[-1]["farmers_arrived"]

        previous_slot_values[
            centre_name
        ] = daily_records[-1]["farmers_arrived"]


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(records)


# ============================================================
# BASIC CLEANING
# ============================================================

df = df.replace(
    [np.inf, -np.inf],
    np.nan
)


df = df.dropna(
    subset=[
        "target_arrivals",
        "target_queue_length",
        "target_waiting_time",
        "target_congestion_score",
        "target_congestion_level"
    ]
)


df = df.reset_index(
    drop=True
)


# ============================================================
# SAVE DATASET
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)


df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 60)
print("GRAINFLOW DATASET CREATED SUCCESSFULLY")
print("=" * 60)

print()
print("Rows    :", len(df))
print("Columns :", len(df.columns))

print()
print("Columns:")
print(df.columns.tolist())

print()
print("First 5 records:")
print(df.head())

print()
print("Dataset saved as:")
print(OUTPUT_PATH)

print()
print("Dataset size:")
print(df.shape)

print()
print("Missing values:")
print(df.isnull().sum().sum())

print()
print("Congestion distribution:")
print(
    df["target_congestion_level"].value_counts()
)

print()
print("Congestion percentages:")
print(
    (
        df["target_congestion_level"]
        .value_counts(normalize=True)
        * 100
    ).round(2)
)

print()
print("=" * 60)
print("DATASET GENERATION COMPLETE")
print("=" * 60)