from src.quality_checks import (
    check_sample_players_quality, 
    check_recommendation_output_quality,
    check_real_player_projections_quality
)
import pandas as pd
import pytest

# test player quality checks
def test_check_sample_players_quality():
    check_sample_players_quality()

# test fail case for duplicate player_id
def test_duplicate_player_id_fails(tmp_path):
    # 1. Create a fake players CSV with duplicate player_id
    fake_players_path = tmp_path / "fake_players.csv"
    fake_players_df = pd.DataFrame({
        "player_id": ["p001", "p001"],
        "player_name": ["Player 1", "Player 1"],
        "position": ["QB", "QB"],
        "projected_points": [100, 100],
        "replacement_points": [50, 50],
    })

    # 2. Create a fake draft picks CSV
    fake_players_df.to_csv(fake_players_path, index=False)
    fake_draft_picks_path = tmp_path / "fake_draft_picks.csv"
    fake_draft_picks_df = pd.DataFrame({
        "round_number": [1],
        "pick_number": [1],
        "team_number": [1],
        "player_id": ["p001"],
    })

    # 3. Save both to tmp_path
    fake_draft_picks_df.to_csv(fake_draft_picks_path, index=False)

    # 4. Run check_sample_players_quality(fake_players_path, fake_draft_picks_path)
    with pytest.raises(ValueError) as error:
        check_sample_players_quality(fake_players_path, fake_draft_picks_path)
    
    # 5. Assert it raises ValueError with the correct error message
    assert "FAILED: Duplicate player_id found in sample_players.csv" in str(error.value)



# test drafted player id
def test_duplicate_drafted_player_id_fails(tmp_path):
    # 1. Create a fake valid players CSV
    fake_players_path = tmp_path / "fake_players.csv"
    fake_players_df = pd.DataFrame({
        "player_id": ["p001"],
        "player_name": ["Player 1"],
        "position": ["QB"],
        "nfl_team":["BUF"],
        "projected_points":[100],
        "replacement_points":[50]
    })

    fake_players_df.to_csv(fake_players_path, index=False)

    # 2. Create a fake draft picks CSV with duplicate drafted player_id
    fake_draft_picks_path = tmp_path / "fake_draft_picks.csv"
    fake_draft_picks_df = pd.DataFrame({
        "round_number": [1, 1],
        "pick_number": [1, 2],
        "team_number": [1, 2],
        "player_id": ["p001", "p001"]
    })
    fake_draft_picks_df.to_csv(fake_draft_picks_path, index=False)

    # 3 Run quality check and expect it to fail
    with pytest.raises(ValueError) as error:
        check_sample_players_quality(fake_players_path, fake_draft_picks_path)
    
    assert "FAILED: Duplicate player_id found in sample_draft_picks.csv" in str(error.value)

# test: Drafted player ID does not exist in sample player pool should fail
def test_not_found_drafted_player(tmp_path):
    # 1. Create a fake valid players CSV
    fake_players_path = tmp_path / "fake_players.csv"
    fake_players_df = pd.DataFrame({
        "player_id": ["101"],
        "player_name": ["Player 1"],
        "position": ["QB"],
        "nfl_team":["BUF"],
        "projected_points":[100],
        "replacement_points":[50]
    })

    fake_players_df.to_csv(fake_players_path, index=False)

    # 2. Create a fake draft picks CSV with duplicate drafted player_id
    # that does NOT exist in the player pool
    fake_draft_picks_path = tmp_path / "fake_draft_picks.csv"
    fake_draft_picks_df = pd.DataFrame({
        "round_number": [1],
        "pick_number": [1],
        "team_number": [1],
        "player_id": ["p999"],
    })

    fake_draft_picks_df.to_csv(fake_draft_picks_path, index=False)

    #3 Run quality check and expect it to fail
    with pytest.raises(ValueError) as error:
        check_sample_players_quality(fake_players_path, fake_draft_picks_path)
    
    assert "FAILED: Drafted player IDs not found in sample_players.csv" in str(error.value)

def test_recommendation_output_quality():
    """
    Positive Test: Test recommendation output and its quality
    """
    check_recommendation_output_quality()

def test_recommendation_output_missing_score_fails(tmp_path):
    """
    Negative Test: Testing recommendation output expecting it to fail
    """
    # Create a fake output CSV
    fake_output_path = tmp_path / "fake_draft_recommendations.csv"

    # Include most columns
    fake_output_df = pd.DataFrame({
        "player_name": ["Player 1"],
        "position": ["QB"],
        "vorp": [50],
        "scarcity_adjustment": [1.25],
        "roster_count": [0],
        "roster_need_adjustment": [8],
        # Intentionally leave out recommendation score (negative test)
        "recommendation_reason": ["High VORP + roster need"]
    })

    fake_output_df.to_csv(fake_output_path, index=False)

    # Run check_recommendation_output_quality(fake_output_path)
    with pytest.raises(ValueError) as error:
        check_recommendation_output_quality(fake_output_path)

    # Expect ValueError
    # Assert the error message with missing required columns
    assert "FAILED: Output is missing required columns" in str(error.value)

def test_drafted_player_in_recommendation_output_fails(tmp_path):
    """
    Negative test:
    If the recommendation output includes p001 and p001 is also in draft picks, the output
    quality check should fail
    """
    #1 Create fake recommendation output CSV
    fake_output_path = tmp_path / "fake_draft_recommendation.csv"

    fake_output_df = pd.DataFrame({
        "player_id": ["p001"],
        "player_name": ["Player 1"],
        "position": ["RB"],
        "vorp": [100],
        "scarcity_adjustment": [1.25],
        "roster_count": [0],
        "roster_need_adjustment": [8],
        "recommendation_score": [109.25],
        "recommendation_reason": ["High VORP + roster need"],
    })

    fake_output_df.to_csv(fake_output_path, index=False)

    # 2. Create fake draft picks CSV where p001 has already been drafted
    fake_draft_picks_path = tmp_path / "fake_draft_picks.csv"

    fake_draft_picks_df = pd.DataFrame({
        "round_number": [1],
        "pick_number": [1],
        "team_number": [1],
        "player_id": ["p001"]
    })

    fake_draft_picks_df.to_csv(fake_draft_picks_path, index=False)

    # 3. Run output quality check and expect it to fail
    with pytest.raises(ValueError) as error:
        check_recommendation_output_quality(
            fake_output_path,
            fake_draft_picks_path
        )

    # 4. Confirm it failed for the expected reason
    assert ("FAILED: Drafted players still appear in the recommendation output") in str(error.value)

def test_real_player_projections_quality_passes(tmp_path):
    """
    Positive test:
    Good real player projections file passes
    """
    fake_real_players_path = tmp_path / "fake_player_projections_2025.csv"

    fake_real_players_df = pd.DataFrame({
        "player_id": ["00-0033873", "00-0036223", "00-0033040"],
        "player_name": ["Christian McCaffrey", "CeeDee Lamb", "Travis Kelce"],
        "position": ["RB", "WR", "TE"],
        "nfl_team": ["SF", "DAL", "KC"],
        "projected_points": [250.5, 230.2, 180.0],
        "replacement_points": [155, 145, 105],
    })

    fake_real_players_df.to_csv(fake_real_players_path, index=False)

    check_real_player_projections_quality(fake_real_players_path)

def test_real_player_projections_duplicate_player_id_fails(tmp_path):
    """
    Negative test:
    Duplicate player_id fails
    """
    fake_real_players_path = tmp_path / "fake_player_projections_2025.csv"

    fake_real_players_df = pd.DataFrame({
        "player_id": ["00-0033873", "00-0033873"],
        "player_name": ["Christian McCaffrey", "Christian McCaffrey"],
        "position": ["RB", "RB"],
        "nfl_team": ["SF", "SF"],
        "projected_points": [250.5, 250.5],
        "replacement_points": [155, 155],
    })

    fake_real_players_df.to_csv(fake_real_players_path, index=False)

    with pytest.raises(ValueError) as error:
        check_real_player_projections_quality(fake_real_players_path)

    assert "FAILED: Player ID has duplicates" in str(error.value)

def test_real_player_projections_bad_position_fails(tmp_path):
    """
    Negative test:
    Bad position fails
    """
    fake_real_players_path = tmp_path / "fake_player_projections_2025.csv"

    fake_real_players_df = pd.DataFrame({
        "player_id": ["00-0033873"],
        "player_name": ["Justin Tucker"],
        "position": ["K"],
        "nfl_team": ["BAL"],
        "projected_points": [140.0],
        "replacement_points": [0],
    })

    fake_real_players_df.to_csv(fake_real_players_path, index=False)

    with pytest.raises(ValueError) as error:
        check_real_player_projections_quality(fake_real_players_path)

    assert "FAILED: Position is not only QB/RB/WR/TE" in str(error.value)