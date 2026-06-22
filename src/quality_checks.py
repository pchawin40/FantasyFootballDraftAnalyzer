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
OUTPUT_PATH = ROOT_DIR / "outputs" / "draft_recommendations.csv"

# read sample players
def check_sample_players_quality(
    players_path=PLAYERS_PATH,
    draft_picks_path=DRAFT_PICKS_PATH
):
    """
    check quality of sample players
    """
    # read sample players from CSV file
    players_df = pd.read_csv(players_path)
    draft_picks_df = pd.read_csv(draft_picks_path)

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

# Validate the final recommendation output
# Goal: Make sure output/draft_recommendations.csv is usable for the dashboard
def check_recommendation_output_quality(
    output_path=OUTPUT_PATH
    ):
    # 1. Output file exists
    if not output_path.exists():
        raise FileNotFoundError("FAILED: Output file does not exist")

    # 2. Output is not empty
    try:
        # read csv
        output_df = pd.read_csv(output_path)
                
        # check if has no rows but headers only
        if output_df.empty:
            raise ValueError("FAILED: The CSV file contains headers but no data rows.")
    
    # If file is completely empty, raise an empty data error
    except pd.errors.EmptyDataError:
        # File is 0 bytes (completely empty)
        raise pd.errors.EmptyDataError("FAILED: The CSV file is completely empty.")

    required_columns = {
        "player_id",
        "player_name",
        "position",
        "vorp",
        "scarcity_adjustment",
        "roster_count",
        "roster_need_adjustment",
        "recommendation_score",
        "recommendation_reason",
    }

    missing_columns = required_columns - set(output_df.columns)

    if missing_columns:
        raise ValueError(f"FAILED: Output is missing required columns: {missing_columns}")

    # 3. recommendation_score has no missing values
    if output_df["recommendation_score"].isna().any():
        raise ValueError("FAILED: Recommendation Score has missing values")

    # 4. recommendation_score is greater than or equal to 0
    if (output_df["recommendation_score"] < 0).any():
        raise ValueError("FAILED: Some recommendation score contains negative value")

    # 5. player_name has no missing values
    if output_df["player_name"].isna().any(): 
        raise ValueError("FAILED: Player name has missing value")

    # 6. no drafted players appear in the recommendation output

    # print passed
    print("PASSED: Recommendation output quality checks passed")

if __name__ == "__main__":
    check_sample_players_quality()
    check_recommendation_output_quality()