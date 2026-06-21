-- Rank available players using VORP plus a simple position scarcity boost
-- Example: If only one RB is available, give a bonus to that RB
-- Example: If many strong WRs are available, no need to give bonus to WRs
-- To answer: Among available players, which positions are drying up?

-- First count how many available players are left at each position
-- Then attach that count back to each available player.
-- Then use that count to calculate a scarcity bonus.
WITH position_summary AS (
    -- count available players by position
    SELECT 
        dp.position,
        COUNT(*) as available_player_count
    FROM dim_player dp
    LEFT JOIN fact_draft_pick fdp USING (player_id)
    WHERE fdp.player_id IS NULL
    GROUP BY dp.position
)
SELECT
    -- player-level output here
    player_name,
    position,
    fp.vorp,
    ps.available_player_count,
    ROUND((10.0 / available_player_count), 2) AS scarcity_adjustment,
    ROUND((fp.vorp + scarcity_adjustment), 2)AS recommendation_score
FROM position_summary ps
JOIN dim_player dp USING (position)
JOIN fact_player_projection fp USING (player_id)
LEFT JOIN fact_draft_pick fdp USING (player_id)
WHERE fdp.player_id IS NULL
ORDER BY 
    recommendation_score DESC,
    player_name ASC;
