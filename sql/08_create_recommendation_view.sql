-- 
CREATE OR REPLACE VIEW recommendation_view AS

-- Select position and roster count at each position
-- for current team (Team 1)
WITH position_summary AS (
    -- count available players by position
    SELECT 
        dp.position,
        COUNT(*) as available_player_count
    FROM dim_player dp
    LEFT JOIN fact_draft_pick fdp USING (player_id)
    WHERE fdp.player_id IS NULL
    GROUP BY dp.position
),
team_roster_summary AS (
    -- count players at each position for current team
    SELECT 
        dp.position,
        COUNT(*) as roster_count
    FROM dim_player dp
    JOIN fact_draft_pick fdp USING (player_id)
    WHERE fdp.team_number = 1
    GROUP BY dp.position
)
SELECT
    -- Select player name, position, vorp, scarcity adjustment, roster count, roster need adjustment, recommendation score
    dp.player_name,
    dp.position,
    fp.vorp,
    ROUND((10.0 / ps.available_player_count), 2) AS scarcity_adjustment,
    COALESCE(trs.roster_count, 0) as roster_count,
    CASE
        WHEN COALESCE(trs.roster_count, 0) = 0 THEN 8
        WHEN COALESCE(trs.roster_count, 0) = 1 THEN 4
        WHEN COALESCE(trs.roster_count, 0) >= 2 THEN 0
    END AS roster_need_adjustment,
    ROUND ((fp.vorp + scarcity_adjustment + roster_need_adjustment), 2) AS recommendation_score,
    CASE
        WHEN fp.vorp >= 100
            AND scarcity_adjustment >= 8
            AND roster_need_adjustment >= 8
        THEN 'High VORP + scarce position + roster need'
        WHEN fp.vorp >= 100
            AND roster_need_adjustment >= 8
        THEN 'High VORP + roster need'
        WHEN scarcity_adjustment >= 8
        THEN 'Scarce position'
        ELSE 'Depth option'
    END AS recommendation_reason
FROM dim_player dp 
JOIN fact_player_projection fp USING (player_id)
LEFT JOIN fact_draft_pick fdp USING (player_id)
LEFT JOIN team_roster_summary trs USING (position)
LEFT JOIN position_summary ps USING (position)
WHERE fdp.player_id IS NULL
ORDER BY 
    recommendation_score DESC,
    player_name ASC;