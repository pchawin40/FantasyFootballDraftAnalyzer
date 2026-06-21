from src.load import load_sample_players, load_draft_picks
from src.export_recommendations import export_draft_recommendations
from src.quality_checks import check_sample_players_quality

def run_pipeline():
    """
    run the pipeline
    """
    # run quality checks
    check_sample_players_quality()
    
    # Load sample players
    load_sample_players()
    
    # load draft picks
    load_draft_picks()

    # export recommendations CSV
    export_draft_recommendations()

    # print success message
    print("Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()