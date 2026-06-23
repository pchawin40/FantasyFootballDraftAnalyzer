from src.extract_nflverse import extract_nfl_data
from src.transform_nflverse import transform_nfl_data
from src.load_real_data import load_real_players
from src.export_recommendations import export_draft_recommendations
from src.quality_checks import (
    check_real_player_projections_quality,
    check_real_draft_picks_quality,
    check_recommendation_output_quality,
    OUTPUT_PATH,
    REAL_DRAFT_PICKS_PATH
)
from src.load_real_draft_picks import load_real_draft_picks

def run_real_data_pipeline():
    """
    run the pipeline for real data
    """
    # extract nfl data
    extract_nfl_data()

    # transform nfl data
    transform_nfl_data()
    
    # check real player projections quality
    check_real_player_projections_quality()

    # check real player drafted quality
    check_real_draft_picks_quality()

    # load real players
    load_real_players()

    # load real draft players
    load_real_draft_picks()

    # export draft recommendations
    export_draft_recommendations()

    # check recommendation output quality
    check_recommendation_output_quality(
        OUTPUT_PATH,
        REAL_DRAFT_PICKS_PATH
    )

    # print success message
    print("Pipeline completed successfully")

if __name__ == "__main__":
    run_real_data_pipeline()