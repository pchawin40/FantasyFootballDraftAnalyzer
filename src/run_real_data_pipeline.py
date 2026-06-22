from src.extract_nflverse import extract_nfl_data
from src.transform_nflverse import transform_nfl_data
from src.load_real_data import load_real_players
from src.load import load_draft_picks
from src.export_recommendations import export_draft_recommendations
from src.quality_checks import check_recommendation_output_quality

def run_real_data_pipeline():
    """
    run the pipeline for real data
    """
    # 1. extract nfl data
    extract_nfl_data()

    # 2. transform nfl data
    transform_nfl_data()

    # 3. load real players
    load_real_players()

    # 4. export draft recommendations
    export_draft_recommendations()

    # 5. check recommendation output quality
    check_recommendation_output_quality()

    # print success message
    print("Pipeline completed successfully")

if __name__ == "__main__":
    run_real_data_pipeline()