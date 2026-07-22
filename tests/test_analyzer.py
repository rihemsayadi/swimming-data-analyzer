import sys
from pathlib import Path

import pandas as pd
import pytest


PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from analyzer import (  # noqa: E402
    calculate_metrics,
    format_pace,
    validate_data,
)


def create_valid_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2026-07-01"],
            "distance_m": [2000],
            "duration_min": [40.0],
            "avg_hr": [150],
            "max_hr": [175],
            "session_type": ["Aerobic"],
            "rpe": [6],
        }
    )


def test_format_pace() -> None:
    assert format_pace(2.5) == "2:30"


def test_calculate_pace() -> None:
    data = create_valid_data()
    result = calculate_metrics(data)

    assert result.loc[0, "pace_min_per_100m"] == 2.0


def test_negative_distance_raises_error() -> None:
    data = create_valid_data()
    data.loc[0, "distance_m"] = -2000

    with pytest.raises(
        ValueError,
        match="distance values",
    ):
        validate_data(data)


def test_invalid_rpe_raises_error() -> None:
    data = create_valid_data()
    data.loc[0, "rpe"] = 12

    with pytest.raises(
        ValueError,
        match="RPE values",
    ):
        validate_data(data)


def test_max_hr_cannot_be_lower_than_avg_hr() -> None:
    data = create_valid_data()
    data.loc[0, "max_hr"] = 140

    with pytest.raises(
        ValueError,
        match="Maximum heart rate",
    ):
        validate_data(data)
        