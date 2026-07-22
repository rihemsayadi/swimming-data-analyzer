from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "swim_sessions.csv"
OUTPUT_DIR = PROJECT_DIR / "output"


def load_data(file_path: Path) -> pd.DataFrame:
    """Load swimming-session data from a CSV file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find: {file_path}")

    return pd.read_csv(file_path)


def validate_data(swim_data: pd.DataFrame) -> None:
    """Check that the dataset contains valid swimming-session data."""
    required_columns = {
        "date",
        "distance_m",
        "duration_min",
        "avg_hr",
        "max_hr",
        "session_type",
        "rpe",
    }

    missing_columns = required_columns - set(swim_data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if swim_data.empty:
        raise ValueError("The swimming dataset is empty.")

    if swim_data.isnull().any().any():
        raise ValueError("The dataset contains missing values.")

    if (swim_data["distance_m"] <= 0).any():
        raise ValueError("All distance values must be greater than zero.")

    if (swim_data["duration_min"] <= 0).any():
        raise ValueError("All duration values must be greater than zero.")

    if (swim_data["avg_hr"] <= 0).any():
        raise ValueError(
            "Average heart-rate values must be greater than zero."
        )

    if (swim_data["max_hr"] <= 0).any():
        raise ValueError(
            "Maximum heart-rate values must be greater than zero."
        )

    if (swim_data["max_hr"] < swim_data["avg_hr"]).any():
        raise ValueError(
            "Maximum heart rate cannot be lower than average heart rate."
        )

    if not swim_data["rpe"].between(1, 10).all():
        raise ValueError("RPE values must be between 1 and 10.")


def calculate_metrics(swim_data: pd.DataFrame) -> pd.DataFrame:
    """Convert dates and calculate pace per 100 metres."""
    result = swim_data.copy()

    result["date"] = pd.to_datetime(
        result["date"],
        errors="raise",
    )

    result["pace_min_per_100m"] = (
        result["duration_min"] / result["distance_m"] * 100
    )

    return result


def format_pace(decimal_minutes: float) -> str:
    """Convert decimal minutes into minutes:seconds format."""
    minutes = int(decimal_minutes)
    seconds = round((decimal_minutes - minutes) * 60)

    if seconds == 60:
        minutes += 1
        seconds = 0

    return f"{minutes}:{seconds:02d}"


def get_overall_summary(swim_data: pd.DataFrame) -> dict:
    """Calculate overall swimming statistics."""
    fastest_session = swim_data.loc[
        swim_data["pace_min_per_100m"].idxmin()
    ]

    longest_session = swim_data.loc[
        swim_data["distance_m"].idxmax()
    ]

    return {
        "number_of_sessions": len(swim_data),
        "total_distance": swim_data["distance_m"].sum(),
        "average_heart_rate": swim_data["avg_hr"].mean(),
        "average_pace": swim_data["pace_min_per_100m"].mean(),
        "fastest_date": fastest_session["date"],
        "fastest_pace": fastest_session["pace_min_per_100m"],
        "longest_date": longest_session["date"],
        "longest_distance": longest_session["distance_m"],
    }


def print_overall_summary(swim_data: pd.DataFrame) -> None:
    """Print the overall swimming summary."""
    summary = get_overall_summary(swim_data)

    print("\nSWIMMING DATA SUMMARY")
    print("---------------------")
    print(f"Number of sessions: {summary['number_of_sessions']}")
    print(f"Total distance: {summary['total_distance']:.0f} m")
    print(
        "Average heart rate: "
        f"{summary['average_heart_rate']:.1f} bpm"
    )
    print(
        "Average pace: "
        f"{format_pace(summary['average_pace'])} per 100 m"
    )
    print(
        "Fastest session: "
        f"{summary['fastest_date'].date()} at "
        f"{format_pace(summary['fastest_pace'])} per 100 m"
    )
    print(
        "Longest session: "
        f"{summary['longest_date'].date()} at "
        f"{summary['longest_distance']:.0f} m"
    )


def get_session_type_summary(
    swim_data: pd.DataFrame,
) -> pd.DataFrame:
    """Group swimming statistics by session type."""
    return (
        swim_data.groupby("session_type")
        .agg(
            sessions=("session_type", "count"),
            total_distance_m=("distance_m", "sum"),
            average_heart_rate=("avg_hr", "mean"),
            average_pace=("pace_min_per_100m", "mean"),
        )
        .reset_index()
    )


def print_session_type_summary(swim_data: pd.DataFrame) -> None:
    """Print statistics for each workout type."""
    summary = get_session_type_summary(swim_data)

    print("\nSUMMARY BY SESSION TYPE")
    print("-----------------------")

    for _, row in summary.iterrows():
        print(f"\n{row['session_type']}")
        print(f"  Sessions: {int(row['sessions'])}")
        print(
            f"  Total distance: "
            f"{row['total_distance_m']:.0f} m"
        )
        print(
            "  Average heart rate: "
            f"{row['average_heart_rate']:.1f} bpm"
        )
        print(
            "  Average pace: "
            f"{format_pace(row['average_pace'])} per 100 m"
        )


def get_weekly_summary(swim_data: pd.DataFrame) -> pd.DataFrame:
    """Group swimming statistics by calendar week."""
    weekly_data = swim_data.copy()

    weekly_data["week_start"] = (
        weekly_data["date"]
        - pd.to_timedelta(
            weekly_data["date"].dt.weekday,
            unit="D",
        )
    )

    return (
        weekly_data.groupby("week_start")
        .agg(
            sessions=("date", "count"),
            total_distance_m=("distance_m", "sum"),
            average_heart_rate=("avg_hr", "mean"),
            average_pace=("pace_min_per_100m", "mean"),
        )
        .reset_index()
        .sort_values("week_start")
    )


def print_weekly_summary(swim_data: pd.DataFrame) -> None:
    """Print weekly swimming statistics."""
    weekly_summary = get_weekly_summary(swim_data)

    print("\nWEEKLY TRAINING SUMMARY")
    print("-----------------------")

    for _, row in weekly_summary.iterrows():
        print(f"\nWeek starting {row['week_start'].date()}")
        print(f"  Sessions: {int(row['sessions'])}")
        print(
            f"  Total distance: "
            f"{row['total_distance_m']:.0f} m"
        )
        print(
            "  Average heart rate: "
            f"{row['average_heart_rate']:.1f} bpm"
        )
        print(
            "  Average pace: "
            f"{format_pace(row['average_pace'])} per 100 m"
        )


def create_pace_graph(swim_data: pd.DataFrame) -> None:
    """Create a graph showing swimming pace over time."""
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
    """Create a graph comparing heart rate and pace."""
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


def create_weekly_distance_graph(
    swim_data: pd.DataFrame,
) -> None:
    """Create a bar graph showing total weekly distance."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    weekly_summary = get_weekly_summary(swim_data)

    plt.figure(figsize=(9, 5))

    plt.bar(
        weekly_summary["week_start"].dt.strftime("%Y-%m-%d"),
        weekly_summary["total_distance_m"],
    )

    plt.title("Weekly Swimming Distance")
    plt.xlabel("Week Starting")
    plt.ylabel("Total Distance (m)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_file = OUTPUT_DIR / "weekly_distance.png"

    plt.savefig(output_file)
    plt.close()

    print(f"Saved graph: {output_file}")


def save_text_report(swim_data: pd.DataFrame) -> None:
    """Save a complete swimming summary to a text file."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    overall = get_overall_summary(swim_data)
    session_types = get_session_type_summary(swim_data)
    weekly_summary = get_weekly_summary(swim_data)

    report_lines = [
        "SWIMMING DATA REPORT",
        "====================",
        "",
        "OVERALL SUMMARY",
        "---------------",
        f"Number of sessions: {overall['number_of_sessions']}",
        f"Total distance: {overall['total_distance']:.0f} m",
        (
            "Average heart rate: "
            f"{overall['average_heart_rate']:.1f} bpm"
        ),
        (
            "Average pace: "
            f"{format_pace(overall['average_pace'])} per 100 m"
        ),
        (
            "Fastest session: "
            f"{overall['fastest_date'].date()} at "
            f"{format_pace(overall['fastest_pace'])} per 100 m"
        ),
        (
            "Longest session: "
            f"{overall['longest_date'].date()} at "
            f"{overall['longest_distance']:.0f} m"
        ),
        "",
        "SUMMARY BY SESSION TYPE",
        "-----------------------",
    ]

    for _, row in session_types.iterrows():
        report_lines.extend(
            [
                "",
                str(row["session_type"]),
                f"Sessions: {int(row['sessions'])}",
                (
                    "Total distance: "
                    f"{row['total_distance_m']:.0f} m"
                ),
                (
                    "Average heart rate: "
                    f"{row['average_heart_rate']:.1f} bpm"
                ),
                (
                    "Average pace: "
                    f"{format_pace(row['average_pace'])} per 100 m"
                ),
            ]
        )

    report_lines.extend(
        [
            "",
            "WEEKLY TRAINING SUMMARY",
            "-----------------------",
        ]
    )

    for _, row in weekly_summary.iterrows():
        report_lines.extend(
            [
                "",
                f"Week starting {row['week_start'].date()}",
                f"Sessions: {int(row['sessions'])}",
                (
                    "Total distance: "
                    f"{row['total_distance_m']:.0f} m"
                ),
                (
                    "Average heart rate: "
                    f"{row['average_heart_rate']:.1f} bpm"
                ),
                (
                    "Average pace: "
                    f"{format_pace(row['average_pace'])} per 100 m"
                ),
            ]
        )

    output_file = OUTPUT_DIR / "swimming_summary.txt"

    output_file.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print(f"Saved report: {output_file}")


def main() -> None:
    try:
        swim_data = load_data(DATA_FILE)
        validate_data(swim_data)
        swim_data = calculate_metrics(swim_data)

        print_overall_summary(swim_data)
        print_session_type_summary(swim_data)
        print_weekly_summary(swim_data)

        create_pace_graph(swim_data)
        create_heart_rate_graph(swim_data)
        create_weekly_distance_graph(swim_data)

        save_text_report(swim_data)

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
    ) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()