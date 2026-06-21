-- Rank available players using VORP plus a simple position scarcity boost
-- Example: If only one RB is available, give a bonus to that RB
-- Example: If many strong WRs are available, no need to give bonus to WRs
-- To answer: Among available players, which positions are drying up?

SELECT 
    position, 
    COUNT(*) AS available_player_count,
    MAX(vorp) AS max_vorp,
    ROUND(AVG(vorp), 2) AS avg_vorp
FROM dim_player dp
JOIN fact_player_projection fp USING (player_id)
GROUP BY position
ORDER BY available_player_count DESC;