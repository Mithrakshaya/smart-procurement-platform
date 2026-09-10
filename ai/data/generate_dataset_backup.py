import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. SETTINGS
# ---------------------------------------------------------

np.random.seed(42)

NUM_DAYS = 200

centres = [
    "C001",
    "C002",
    "C003",
    "C004",
    "C005"
]

time_slots = [
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00"
]

crop_types = [
    "Rice",
    "Wheat",
    "Maize",
    "Cotton",
    "Groundnut"
]

weather_types = [
    "Normal",
    "Cloudy",
    "Rainy",
    "Hot"
]

# Different centres have different capacities
centre_capacity = {
    "C001": 40,
    "C002": 50,
    "C003": 35,
    "C004": 60,
    "C005": 45
}

# Different centres have slightly different workload levels
centre_factor = {
    "C001": 1.00,
    "C002": 1.15,
    "C003": 0.90,
    "C004": 1.25,
    "C005": 1.05
}


# ---------------------------------------------------------
# 2. GENERATE RECORDS
# ---------------------------------------------------------

records = []

start_date = datetime(2025, 1, 1)

# Store previous arrivals for historical features
previous_day_totals = {
    centre: 50 for centre in centres
}

previous_slot_arrivals = {
    centre: 10 for centre in centres
}

previous_queue = {
    centre: 0 for centre in centres
}


for day_number in range(NUM_DAYS):

    current_date = start_date + timedelta(days=day_number)

    day_of_week_number = current_date.weekday()

    day_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_of_week = day_names[day_of_week_number]

    # Weekend indicator
    weekend = 1 if day_of_week_number >= 5 else 0

    # Harvest season
    month = current_date.month

    harvest_season = (
        "Yes"
        if month in [1, 2, 3, 10, 11, 12]
        else "No"
    )

    # Simulated holidays
    holiday = 1 if np.random.random() < 0.05 else 0


    for centre in centres:

        capacity = centre_capacity[centre]
        c_factor = centre_factor[centre]

        daily_arrivals = 0


        for slot_index, time_slot in enumerate(time_slots):

            # -------------------------------------------------
            # 3. TIME-BASED DEMAND
            # -------------------------------------------------

            # Morning and late-morning slots are generally busier
            slot_demand = {
                0: 0.75,
                1: 0.95,
                2: 1.20,
                3: 1.30,
                4: 1.10,
                5: 0.90,
                6: 0.75,
                7: 0.55
            }[slot_index]


            # Weekend usually has slightly lower activity
            weekend_factor = 0.85 if weekend else 1.0

            # Harvest season increases farmer arrivals
            season_factor = 1.25 if harvest_season == "Yes" else 1.0

            # Holidays reduce normal operations
            holiday_factor = 0.65 if holiday else 1.0


            # -------------------------------------------------
            # 4. WEATHER
            # -------------------------------------------------

            weather = np.random.choice(
                weather_types,
                p=[0.55, 0.20, 0.15, 0.10]
            )

            if weather == "Normal":
                temperature = np.random.normal(27, 2)
                rainfall = max(0, np.random.normal(1, 2))
                weather_factor = 1.0

            elif weather == "Cloudy":
                temperature = np.random.normal(25, 2)
                rainfall = max(0, np.random.normal(5, 4))
                weather_factor = 0.95

            elif weather == "Rainy":
                temperature = np.random.normal(23, 2)
                rainfall = max(5, np.random.normal(20, 8))
                weather_factor = 0.75

            else:
                temperature = np.random.normal(34, 2)
                rainfall = max(0, np.random.normal(0.5, 1))
                weather_factor = 0.85


            # -------------------------------------------------
            # 5. EXPECTED FARMER ARRIVALS
            # -------------------------------------------------

            base_arrivals = 18

            expected_arrivals = (
                base_arrivals
                * slot_demand
                * weekend_factor
                * season_factor
                * holiday_factor
                * weather_factor
                * c_factor
            )

            # Historical information influences today's arrivals
            historical_effect = (
                0.08 * previous_day_totals[centre]
                + 0.15 * previous_slot_arrivals[centre]
            )

            expected_arrivals += historical_effect

            # Random variation
            farmers_arrived = max(
                0,
                int(np.random.normal(expected_arrivals, 4))
            )


            # -------------------------------------------------
            # 6. BOOKED SLOTS
            # -------------------------------------------------

            booking_ratio = np.random.uniform(0.75, 1.05)

            booked_slots = int(
                max(
                    0,
                    min(
                        capacity,
                        farmers_arrived * booking_ratio
                        + np.random.normal(5, 3)
                    )
                )
            )


            # -------------------------------------------------
            # 7. CROP AND QUANTITY
            # -------------------------------------------------

            crop_type = np.random.choice(
                crop_types,
                p=[0.35, 0.15, 0.20, 0.15, 0.15]
            )

            crop_quantity = {
                "Rice": np.random.normal(35, 8),
                "Wheat": np.random.normal(30, 7),
                "Maize": np.random.normal(40, 10),
                "Cotton": np.random.normal(25, 6),
                "Groundnut": np.random.normal(28, 7)
            }[crop_type]

            quantity = round(max(5, crop_quantity), 2)


            # -------------------------------------------------
            # 8. PROCUREMENT TIME
            # -------------------------------------------------

            crop_time_factor = {
                "Rice": 1.00,
                "Wheat": 0.95,
                "Maize": 1.10,
                "Cotton": 1.20,
                "Groundnut": 1.05
            }[crop_type]

            average_procurement_time = (
                18
                * crop_time_factor
                * (1.10 if weather == "Rainy" else 1.0)
            )

            average_procurement_time += np.random.normal(0, 2)

            average_procurement_time = round(
                max(8, average_procurement_time),
                2
            )


            # -------------------------------------------------
            # 9. QUEUE LENGTH
            # -------------------------------------------------

            service_capacity = max(
                1,
                int(capacity * 0.55)
            )

            queue_change = (
                farmers_arrived
                - service_capacity
            )

            queue_length = max(
                0,
                int(
                    previous_queue[centre]
                    + queue_change
                    + np.random.normal(0, 2)
                )
            )


            # -------------------------------------------------
            # 10. WAITING TIME
            # -------------------------------------------------

            average_waiting_time = (
                queue_length
                * average_procurement_time
                / max(service_capacity, 1)
            )

            average_waiting_time += np.random.normal(5, 3)

            average_waiting_time = round(
                max(0, average_waiting_time),
                2
            )


            # -------------------------------------------------
            # 11. CONGESTION SCORE
            # -------------------------------------------------

            utilization = (
                (booked_slots + queue_length)
                / capacity
            )

            congestion_score = (
                utilization * 70
                + (average_waiting_time / 60) * 30
            )

            congestion_score = round(
                min(100, max(0, congestion_score)),
                2
            )


            if congestion_score < 40:
                congestion_level = "LOW"

            elif congestion_score < 70:
                congestion_level = "MEDIUM"

            else:
                congestion_level = "HIGH"


            # -------------------------------------------------
            # 12. SAVE RECORD
            # -------------------------------------------------

            records.append({

                "date": current_date.strftime("%Y-%m-%d"),

                "day_of_week": day_of_week,

                "centre_id": centre,

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

                "temperature":
                    round(temperature, 2),

                "rainfall":
                    round(rainfall, 2),

                "harvest_season":
                    harvest_season,

                "holiday":
                    holiday,

                "previous_day_arrivals":
                    previous_day_totals[centre],

                "previous_slot_arrivals":
                    previous_slot_arrivals[centre],

                # Prediction targets
                "target_arrivals":
                    farmers_arrived,

                "target_queue_length":
                    queue_length,

                "target_waiting_time":
                    average_waiting_time,

                "target_congestion_score":
                    congestion_score,

                "target_congestion_level":
                    congestion_level
            })


            # Update historical information
            previous_slot_arrivals[centre] = farmers_arrived
            previous_queue[centre] = queue_length

            daily_arrivals += farmers_arrived


        # Update previous day's arrivals
        previous_day_totals[centre] = daily_arrivals


# ---------------------------------------------------------
# 13. CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(records)


# ---------------------------------------------------------
# 14. SAVE DATASET
# ---------------------------------------------------------

output_file = "grainflow_historical_data.csv"

df.to_csv(output_file, index=False)


# ---------------------------------------------------------
# 15. DISPLAY INFORMATION
# ---------------------------------------------------------

print("=" * 60)
print("GRAINFLOW DATASET CREATED SUCCESSFULLY")
print("=" * 60)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nDataset saved as:")
print(output_file)

print("\nDataset size:")
print(df.shape)