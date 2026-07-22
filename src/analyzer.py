from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "swim_sessions.csv"


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find: {file_path}")

    return pd.read_csv(file_path)

def format_pace(decimal_minutes: float) -> str:
    minutes = int(decimal_minutes)
    seconds = round((decimal_minutes - minutes) * 60)

    if seconds == 60:
        minutes += 1
        seconds = 0

    return f"{minutes}:{seconds:02d}"

def main() -> None:
    try:
        swim_data = load_data(DATA_FILE)

        swim_data["pace_min_per_100m"] = (
            swim_data["duration_min"] / swim_data["distance_m"] * 100
        )

        total_distance = swim_data["distance_m"].sum()
        average_heart_rate = swim_data["avg_hr"].mean()
        average_pace = swim_data["pace_min_per_100m"].mean()
        fastest_session = swim_data.loc[
             swim_data["pace_min_per_100m"].idxmin()
             ]
        longest_session = swim_data.loc[
             swim_data["distance_m"].idxmax()
             ]

        print("\nSWIMMING DATA SUMMARY")
        print("---------------------")
        print(f"Number of sessions: {len(swim_data)}")
        print(f"Total distance: {total_distance:.0f} m")
        print(f"Average heart rate: {average_heart_rate:.1f} bpm")
        print(f"Average pace: {format_pace(average_pace)} per 100 m")
        print(
            f"Fastest session: {fastest_session['date']} "
            f"at {format_pace(fastest_session['pace_min_per_100m'])} per 100 m"
            )
        print(
            f"Longest session: {longest_session['date']} "
            f"at {longest_session['distance_m']:.0f} m"
        )
    except FileNotFoundError as error:
        print(f"Error: {error}")
if __name__ == "__main__":
    main()