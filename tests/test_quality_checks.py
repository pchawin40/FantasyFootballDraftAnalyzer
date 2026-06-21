from src.quality_checks import check_sample_players_quality
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
    fake_draft_picks_df.to_csv(fake_draft_picks_path, index=False)

    # 3. Save both to tmp_path
    fake_players_df.to_csv(fake_players_path, index=False)
    fake_draft_picks_df.to_csv(fake_draft_picks_path, index=False)

    # 4. Run check_sample_players_quality(fake_players_path, fake_draft_picks_path)
    with pytest.raises(ValueError) as error:
        check_sample_players_quality(fake_players_path, fake_draft_picks_path)
    
    # 5. Assert it raises ValueError with the correct error message
    assert "FAILED: Duplicate player_id found in sample_players.csv" in str(error.value)
