import pandas as pd
from pathlib import Path

from predict_arrivals import predict_arrivals
from predict_queue import predict_queue
from predict_waiting_time import predict_waiting_time
from predict_congestion import predict_congestion, get_congestion_level


# --------------------------------------------------
# PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "grainflow_features.csv"
)


# --------------------------------------------------
# RECOMMEND BEST SLOT
# --------------------------------------------------

def recommend_slot(df):

    results = []

    # Get available slots
    slots = sorted(df["time_slot"].unique())

    for slot in slots:

        slot_data = df[
            df["time_slot"] == slot
        ].iloc[[0]].copy()

        # Farmer arrival prediction
        arrival_prediction = predict_arrivals(
            slot_data
        )[0]

        # Queue prediction
        queue_prediction = predict_queue(
            slot_data
        )[0]

        # Waiting-time prediction
        waiting_prediction = predict_waiting_time(
            slot_data
        )[0]

        # Congestion prediction
        congestion_prediction = predict_congestion(
            slot_data
        )[0]

        congestion_level = get_congestion_level(
            congestion_prediction
        )

        # --------------------------------------------------
        # SLOT SCORE
        # Lower score = better slot
        # --------------------------------------------------

        score = (
            congestion_prediction * 0.50
            + queue_prediction * 0.25
            + waiting_prediction * 0.25
        )

        results.append({
            "time_slot": slot,
            "predicted_arrivals": round(
                arrival_prediction, 2
            ),
            "predicted_queue": round(
                queue_prediction, 2
            ),
            "predicted_waiting_time": round(
                waiting_prediction, 2
            ),
            "congestion_score": round(
                congestion_prediction, 2
            ),
            "congestion_level": congestion_level,
            "slot_score": round(
                score, 2
            )
        })

    # Convert to DataFrame
    results_df = pd.DataFrame(results)

    # Best slot = lowest score
    best_slot = results_df.loc[
        results_df["slot_score"].idxmin()
    ]

    return results_df, best_slot


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("\n======================================")
    print("SMART SLOT RECOMMENDATION")
    print("======================================")

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    print(
        "Dataset loaded:",
        df.shape
    )

    # Select one centre
    centre_id = df[
        "centre_id"
    ].iloc[0]

    centre_data = df[
        df["centre_id"] == centre_id
    ].copy()

    print(
        "\nCentre selected:",
        centre_id
    )

    # Generate recommendation
    results, best_slot = recommend_slot(
        centre_data
    )

    print("\nSlot predictions:")
    print(results.to_string(index=False))

    print("\n======================================")
    print("RECOMMENDED SLOT")
    print("======================================")

    print(
        "Best time slot:",
        best_slot["time_slot"]
    )

    print(
        "Predicted arrivals:",
        best_slot["predicted_arrivals"]
    )

    print(
        "Predicted queue:",
        best_slot["predicted_queue"]
    )

    print(
        "Predicted waiting time:",
        best_slot["predicted_waiting_time"]
    )

    print(
        "Congestion score:",
        best_slot["congestion_score"]
    )

    print(
        "Congestion level:",
        best_slot["congestion_level"]
    )

    print("\nSmart slot recommendation working successfully!")