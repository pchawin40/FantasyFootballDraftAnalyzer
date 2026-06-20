# from ../src/projections import calculate_half_ppr_points, calculate_vorp
from src.projections import calculate_half_ppr_points, calculate_vorp

def test_calculate_half_ppr_points():
    scoring = {
        "receiving_yards": 0.1,
        "receiving_td": 6,
        "reception": 0.5,
    }

    player_stats = {
        "receiving_yards": 100,
        "receiving_td": 1,
        "reception": 6,
    }

    result = calculate_half_ppr_points(player_stats, scoring)

    ## (100 * 0.1) + (1 * 6) + (6 * 0.5) = 10 + 6 + 3 = 19
    assert result == 19.0

def test_calculate_vorp():
    result = calculate_vorp(projected_points = 250, replacement_points = 180)

    assert result == 70.0