import pandas as pd
import nflreadpy as nfl
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
RAW_OUTPUT_PATH = RAW_DIR / "player_stats_2025.csv"

def extract_nfl_data():
    """
    Goal: Pull one season of real player stats into data/raw/player_stats_2025.csv
    """
    print("Fetching datasets from nflverse...")

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

    # Save raw file
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_OUTPUT_PATH, index=False)

    print(f"Saved raw player stats to {RAW_OUTPUT_PATH}")

    # 3. Filter to offensive fantasy positions: QB, RB, WR, TE
    
    # filter by positions    

    # 4. Save raw file to data/raw/player_stats_2025.csv

    # 5. Print row count and column count

if __name__ == "__main__":
    extract_nfl_data()