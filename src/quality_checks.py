# This file checks input data quality and consistency
# Quality to check for:
# 1. No duplicate player_id in sample_players.csv
# 2. No missing player_name
# 3. No missing position
# 4. Projected points must be greater than or equal to 0
# 5. Replacement points must be greater than or equal to 0
# 6. Every drafted player id must exists in sample players.csv
# 7. No duplicate drafted player_id in sample_draft_picks.csv

# import libraries
import pandas as pd
from pathlib import Path

# set root directory
ROOT_DIR = Path(__file__).resolve().parents[1]
PLAYERS_PATH = ROOT_DIR / "data" / "sample_players.csv"
DRAFT_PICKS_PATH = ROOT_DIR / "data" / "sample_draft_picks.csv"

# read sample players
def check_sample_players_quality():
    """
    check quality of sample players
    """
    # read sample players from CSV file
    players_df = pd.read_csv(PLAYERS_PATH)
    draft_picks_df = pd.read_csv(DRAFT_PICKS_PATH)

    # check for duplicate player_id
    if draft_picks_df["player_id"].duplicated().any():
        raise ValueError("FAILED: Duplicate player_id found in sample_draft_picks.csv")
    else: 
        print("PASSED: No duplicate player_id values in sample_draft_picks.csv")
    
    if players_df["player_id"].duplicated().any():
        raise ValueError("FAILED: Duplicate player_id found in sample_players.csv")
    else:
        print("PASSED: No duplicate player_id values in sample_players.csv")
    
    # No missing player_name
    if players_df["player_name"].isnull().any():
        raise ValueError("FAILED: Missing player_name values")
    else: 
        print("PASSED: No missing player names")
    
    # No missing position
    if players_df["position"].isnull().any():
        raise ValueError("FAILED: Missing position values")
    else:
        print("PASSED: No missing positions")
    
    # Projected points must be greater than or equal to 0
    if players_df["projected_points"].lt(0).any():
        raise ValueError("FAILED: Projected points must be greater than or equal to 0")
    else:
        print("PASSED: Projected points are all greater than or equal to 0")

    # Replacement points must be greater than or equal to 0
    if players_df["replacement_points"].lt(0).any():
        raise ValueError("FAILED: Replacement points must be greater than or equal to 0")
    else:
        print("PASSED: Replacement points are all greater than or equal to 0")

    # Check which drafted player IDs do not exist in the player pool?
    missing_player_ids = set(draft_picks_df["player_id"]) - set(players_df["player_id"])
    
    if not missing_player_ids:
        print("PASSED: Every drafted player id exists in sample_players.csv")
    else:
        raise ValueError(f"FAILED: Drafted player IDs not found in sample_players.csv: {missing_player_ids}")

if __name__ == "__main__":
    check_sample_players_quality()