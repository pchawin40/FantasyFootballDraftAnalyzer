-- Step 1. Clear old test draft picks
DELETE FROM fact_draft_pick;

-- Step 2. Insert fake drafted players
INSERT INTO fact_draft_pick 
(
    draft_pick_id,
    round_number,
    pick_number,
    team_number,
    player_id
) 
VALUES 
(1, 1, 1, 1, 'p001'),
(2, 1, 2, 2, 'p002'),
(3, 1, 3, 3, 'p003');

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