CREATE TABLE IF NOT EXISTS dim_player (
    player_id TEXT PRIMARY KEY,
    player_name TEXT NOT NULL,
    position TEXT NOT NULL,
    nfl_team TEXT
);

CREATE TABLE IF NOT EXISTS fact_player_projection(
    projection_id INTEGER PRIMARY KEY,
    player_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    projected_points REAL NOT NULL,
    replacement_points REAL NOT NULL,
    vorp REAL NOT NULL,
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id)
);

CREATE TABLE IF NOT EXISTS fact_draft_pick(
    draft_pick_id INTEGER PRIMARY KEY,
    round_number INTEGER NOT NULL,
    pick_number INTEGER NOT NULL,
    team_number INTEGER NOT NULL,
    player_id TEXT,
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id)
);