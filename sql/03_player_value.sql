SELECT 
    dp.player_name,
    dp.position,
    dp.nfl_team,
    fp.projected_points, 
    fp.replacement_points,
    fp.vorp
FROM dim_player dp
JOIN fact_player_projection fp USING (player_id)
ORDER BY fp.vorp DESC;