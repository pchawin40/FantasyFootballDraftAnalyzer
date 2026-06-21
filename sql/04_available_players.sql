-- Select players not yet drafted
SELECT
    dp.player_name,
    dp.position,
    dp.nfl_team,
    fp.projected_points,
    fp.replacement_points,
    fp.vorp
FROM dim_player dp
JOIN fact_player_projection fp USING (player_id)
LEFT JOIN fact_draft_pick fdp USING (player_id)
WHERE fdp.player_id IS NULL
ORDER BY fp.vorp DESC;