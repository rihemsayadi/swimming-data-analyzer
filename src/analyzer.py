from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "swim_sessions.csv"


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find: {file_path}")

    return pd.read_csv(file_path)


def main() -> None:
    try:
        swim_data = load_data(DATA_FILE)

        print("Swimming data loaded successfully.\n")
        print(swim_data)

    except FileNotFoundError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
    