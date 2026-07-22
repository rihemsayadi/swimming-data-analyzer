
# Swimming Data Analyzer

A Python project that analyzes swimming-session data and generates
training summaries, weekly statistics, graphs, and a text report.

## Motivation

I created this project to combine my competitive swimming background
with my interest in biomedical engineering, physiological data, and
software development.

## Features

- Imports swimming sessions from a CSV file
- Validates required columns and numerical values
- Calculates pace per 100 metres
- Calculates total distance and average heart rate
- Identifies the fastest and longest sessions
- Compares different workout types
- Generates weekly training summaries
- Creates pace, heart-rate, and weekly-distance graphs
- Exports a complete text report
- Includes automated tests

## Technologies

- Python
- pandas
- matplotlib
- pytest
- Git
- GitHub

## Project Structure

```text
swimming-data-analyzer/
├── data/
│   └── swim_sessions.csv
├── output/
│   ├── heart_rate_vs_pace.png
│   ├── pace_over_time.png
│   ├── swimming_summary.txt
│   └── weekly_distance.png
├── src/
│   └── analyzer.py
├── tests/
│   └── test_analyzer.py
├── README.md
├── requirements.txt
└── .gitignore