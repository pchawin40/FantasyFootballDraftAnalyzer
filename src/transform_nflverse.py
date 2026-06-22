import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

RAW_INPUT_PATH = ROOT_DIR / "data" / "raw" / "player_stats_2025_fantasy_positions.csv"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
PROCESSED_OUTPUT_PATH = PROCESSED_DIR / "player_projections_2025.csv"

def transform_nfl_data():
    """
    Calculate fantasy points and turn real stats into model format
    
    - Extract raw NFL data
    - create a clean model-ready file as "player_projections_2025.csv"
    """

    # 0. print message to console
    print("Transforming 2025 NFL data into model-ready format...")

    # 1. Read raw fantasy-position player stats
    df = pd.read_csv(RAW_INPUT_PATH)

    print("Raw filtered data shape:")
    print(df.shape)

    print("Available columns:")
    print(df.columns.tolist())

    # 2. Keep only fantasy positions
    fantasy_positions = ["QB", "RB", "WR", "TE"]
    df = df[df["position"].isin(fantasy_positions)].copy()

    # 3. Inspect columns before calculating fantasy points
    print("Position counts:")
    print(df["position"].value_counts())

    print("Preview:")
    print(df.head())

    # 4. Save a temporary transformed preview
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_OUTPUT_PATH, index=False)

    print(f"Saved transformed preview to {PROCESSED_OUTPUT_PATH}")

if __name__ == "__main__":
    transform_nfl_data()

