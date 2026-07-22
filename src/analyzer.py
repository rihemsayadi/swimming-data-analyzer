from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "swim_sessions.csv"
OUTPUT_DIR = PROJECT_DIR / "output"


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
def create_pace_graph(swim_data: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(9, 5))
    plt.plot(
        swim_data["date"],
        swim_data["pace_min_per_100m"],
        marker="o",
    )

    plt.title("Swimming Pace Over Time")
    plt.xlabel("Date")
    plt.ylabel("Pace (minutes per 100 m)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_file = OUTPUT_DIR / "pace_over_time.png"
    plt.savefig(output_file)
    plt.close()

    print(f"Saved graph: {output_file}")
def create_heart_rate_graph(swim_data: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.scatter(
        swim_data["avg_hr"],
        swim_data["pace_min_per_100m"],
    )

    plt.title("Heart Rate Versus Swimming Pace")
    plt.xlabel("Average Heart Rate (bpm)")
    plt.ylabel("Pace (minutes per 100 m)")
    plt.tight_layout()

    output_file = OUTPUT_DIR / "heart_rate_vs_pace.png"
    plt.savefig(output_file)
    plt.close()

    print(f"Saved graph: {output_file}")    

def print_session_type_summary(swim_data: pd.DataFrame) -> None:
    summary = (
        swim_data.groupby("session_type")
        .agg(
            sessions=("session_type", "count"),
            total_distance_m=("distance_m", "sum"),
            average_heart_rate=("avg_hr", "mean"),
            average_pace=("pace_min_per_100m", "mean"),
        )
        .reset_index()
    )

    print("\nSUMMARY BY SESSION TYPE")
    print("-----------------------")

    for _, row in summary.iterrows():
        print(f"\n{row['session_type']}")
        print(f"  Sessions: {int(row['sessions'])}")
        print(f"  Total distance: {row['total_distance_m']:.0f} m")
        print(f"  Average heart rate: {row['average_heart_rate']:.1f} bpm")
        print(
            "  Average pace: "
            f"{format_pace(row['average_pace'])} per 100 m"
        )

def main() -> None:
    try:
        swim_data = load_data(DATA_FILE)

        swim_data["pace_min_per_100m"] = (
            swim_data["duration_min"] / swim_data["distance_m"] * 100
        )

        total_distance = swim_data["distance_m"].sum()
        average_heart_rate = swim_data["avg_hr"].mean()
        average_pace = swim_data["pace_min_per_100m"].mean()
        swim_data["date"] = pd.to_datetime(swim_data["date"])
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
        print_session_type_summary(swim_data)
        create_pace_graph(swim_data)
        create_heart_rate_graph(swim_data)
    except FileNotFoundError as error:
        print(f"Error: {error}")
if __name__ == "__main__":
    main()