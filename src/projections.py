def calculate_half_ppr_points(player_stats: dict, scoring: dict) -> float:
    """
    Calculate fantasy points using half-PPR scoring system
    """
    points = 0

    points += player_stats.get("passing_yards", 0) * scoring.get("passing_yards", 0)
    points += player_stats.get("passing_td", 0) * scoring.get("passing_td", 0)
    points += player_stats.get("interception", 0) * scoring.get("interception", 0)
    
    points += player_stats.get("rushing_yards", 0) * scoring.get("rushing_yards", 0)
    points += player_stats.get("rushing_td", 0) * scoring.get("rushing_td", 0)
    
    points += player_stats.get("receiving_yards", 0) * scoring.get("receiving_yards", 0)
    points += player_stats.get("receiving_td", 0) * scoring.get("receiving_td", 0)
    points += player_stats.get("reception", 0) * scoring.get("reception", 0)
    
    points += player_stats.get("fumble_lost", 0) * scoring.get("fumble_lost", 0)
    
    return round(points, 2)

def calculate_vorp(projected_points: float, replacement_points: float) -> float:
    """
    Calculate value over replacement player
    """

    return round(projected_points - replacement_points, 2)
