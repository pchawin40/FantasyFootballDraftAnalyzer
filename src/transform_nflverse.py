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
    
    # 2. Keep only fantasy positions
    fantasy_positions = ["QB", "RB", "WR", "TE"]
    df = df[df["position"].isin(fantasy_positions)].copy()

    # 3. Inspect columns before calculating fantasy points
    print("Position counts:")
    print(df["position"].value_counts())

    # 4. Group weekly player stats into one season-level row per player
    season_df = (
        df.groupby(
            ["player_id", "player_display_name", "position", "team"],
            as_index=False
        )
        .agg({
            "fantasy_points": "sum"
        })
    )

    season_df = season_df.rename(columns={
        "player_display_name": "player_name",
        "team": "nfl_team",
        "fantasy_points": "projected_points",
    })

    # 5. Add replacement level points by position
    replacement_points_by_position = {
        "QB": 260,
        "RB": 155,
        "WR": 145,
        "TE": 105,
    }

    season_df["replacement_points"] = season_df["position"].map(replacement_points_by_position)

    # 6. Confirm every position received replacement points
    if season_df["replacement_points"].isna().any():
        missing_positions = season_df.loc[
            season_df["replacement_points"].isna(),
            "position"
        ].unique()

        raise ValueError(f"FAILED: Missing replacement points for positions: {missing_positions}")

    # 7. Keep only model ready columns
    season_df = season_df[
        [
            "player_id",
            "player_name",
            "position",
            "nfl_team",
            "projected_points",
            "replacement_points",
        ]
    ].copy()

    # 8. Sort by projected points
    season_df = season_df.sort_values("projected_points", ascending=False)

    # 9. Save a model-ready file
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    season_df.to_csv(PROCESSED_OUTPUT_PATH, index=False)

    print("Processed player projection shape:")
    print(season_df.shape)

    print("Processed player projection preview:")
    print(season_df.head())

    print("Available columns:")
    print(season_df.columns.tolist())

    print(f"Saved model-ready projections to {PROCESSED_OUTPUT_PATH}")


if __name__ == "__main__":
    transform_nfl_data()

