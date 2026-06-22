import pandas as pd
import nflreadpy as nfl
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
RAW_OUTPUT_PATH = RAW_DIR / "player_stats_2025.csv"
FILTERED_OUTPUT_PATH = RAW_DIR / "player_stats_2025_fantasy_positions.csv"

def extract_nfl_data():
    """
    Pull one season of real player stats into data/raw/player_stats_2025.csv
    """
    # 0. print message to console
    print("Fetching 2025 player stats from nflverse...")

    # 1. Load player stats from nflverse using nflreadpy
    player_stats = nfl.load_player_stats(2025)

    # 2. Read player stats into pandas
    if hasattr(player_stats, "to_pandas"):
        df = player_stats.to_pandas()
    else:
        df = player_stats

    # 3. Inspect the raw data
    print("Raw player stats shape: ")
    print(df.shape)

    print("Raw player stats columns")
    print(df.columns.tolist())

    print("raw player stats preview")
    print(df.head())

    # 4. Save raw file
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_OUTPUT_PATH, index=False)

    print(f"Saved raw player stats to {RAW_OUTPUT_PATH}")

    # 5. Save a filtered version for fantasy positions
    fantasy_positions = ["QB", "RB", "WR", "TE"]

    if "position" not in df.columns:
        raise ValueError("FAILED: Expected column 'position' was not found in player stats data")
    
    fantasy_df = df[df["position"].isin(fantasy_positions)].copy()

    fantasy_df.to_csv(FILTERED_OUTPUT_PATH, index=False)

    print("Filtered fantasy-position player stats shape:")
    print(fantasy_df.shape)

    print(f"Saved filterd fantasy player stats to {FILTERED_OUTPUT_PATH}")

if __name__ == "__main__":
    extract_nfl_data()