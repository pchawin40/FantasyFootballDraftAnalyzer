from src.extract_nflverse import extract_nfl_data
from src.transform_nflverse import transform_nfl_data
from src.load_real_data import load_real_players
from src.export_recommendations import export_draft_recommendations
from src.quality_checks import check_real_player_projections_quality

def run_real_data_pipeline():
    """
    run the pipeline for real data
    """
    # 1. extract nfl data
    extract_nfl_data()

    # 2. transform nfl data
    transform_nfl_data()
    
    # 3. check real player projections quality
    check_real_player_projections_quality()

    # 4. load real players
    load_real_players()

    # 5. export draft recommendations
    export_draft_recommendations()


    # print success message
    print("Pipeline completed successfully")

if __name__ == "__main__":
    run_real_data_pipeline()