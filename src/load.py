# Create a local DuckDB database and load sample players
import duckdb
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
PLAYERS_PATH = ROOT_DIR / "data" / "sample_players.csv"
DRAFT_PICKS_PATH = ROOT_DIR / "data" / "sample_draft_picks.csv"
DB_PATH = ROOT_DIR / "fantasy_football.duckdb"
SCHEMA_PATH = ROOT_DIR / "sql" / "01_schema.sql"

def load_sample_players():
    """
    load sample players from CSV file into DuckDB database
    """
    df = pd.read_csv(PLAYERS_PATH)

    df["season"] = 2026
    df["vorp"] = df["projected_points"] - df["replacement_points"]

    players_df = df [["player_id", "player_name", "position", "nfl_team"]]

    projections_df = df [
        [
            "player_id",
            "season",
            "projected_points",
            "replacement_points",
            "vorp",
        ]
    ].copy()

    projections_df.insert(0, "projection_id", range(1, len(projections_df) + 1))

    with duckdb.connect(DB_PATH) as con:
        schema_sql = SCHEMA_PATH.read_text()
        con.execute(schema_sql)

        con.execute("DELETE FROM fact_draft_pick")
        con.execute("DELETE FROM fact_player_projection")
        con.execute("DELETE FROM dim_player")

        con.register("players_df", players_df)
        con.register("projections_df", projections_df)

        con.execute("INSERT INTO dim_player SELECT * FROM players_df")
        con.execute("INSERT INTO fact_player_projection SELECT * FROM projections_df")

        result = con.execute(
            """
            SELECT
                p.player_name,
                p.position,
                p.nfl_team,
                fp.projected_points,
                fp.replacement_points,
                fp.vorp
            FROM fact_player_projection fp
            JOIN dim_player p USING (player_id)
            ORDER BY fp.vorp DESC
            """
        ).fetchdf()

        # print sample players result
        print("Sample Players Result:")
        print(result)
        print("--------------------------------")

def load_draft_picks():
    """
    load draft picks from CSV file into DuckDB database
    """
    # read draft picks from CSV file
    df = pd.read_csv(DRAFT_PICKS_PATH)

    # add columns draft_pick_id, round_number, pick_number, team_number
    draft_players_df = df [
        [
            "round_number", 
            "pick_number", 
            "team_number", 
            "player_id"
        ]
    ].copy()

    # insert draft pick columns
    draft_players_df.insert(0, "draft_pick_id", range(1, len(draft_players_df) + 1))

    # register draft picks dataframe
    with duckdb.connect(DB_PATH) as con:
        schema_sql = SCHEMA_PATH.read_text()
        con.execute(schema_sql)

        # insert draft picks into database
        con.register("draft_players_df", draft_players_df)

        con.execute("INSERT INTO fact_draft_pick SELECT * FROM draft_players_df")

        draft_picks_result = con.execute(
            """
            SELECT
                fdp.draft_pick_id,
                fdp.round_number,
                fdp.pick_number,
                fdp.team_number,
                fdp.player_id
            FROM fact_draft_pick fdp
            ORDER BY fdp.draft_pick_id ASC
            """
        ).fetchdf()

        # print draft picks result
        print("Draft Players Result:")
        print(draft_picks_result)
        print("--------------------------------")

def load_available_players():
    """
    load available players from DuckDB database
    """
    # read available players from CSV file
    df = pd.read_csv(PLAYERS_PATH)

    df["season"] = 2026
    df["vorp"] = df["projected_points"] - df["replacement_points"]

    # create dataframe for available players
    available_players_df = df [["player_id", "player_name", "position", "nfl_team"]]

    available_players_projections_df = df [
        [
            "player_id",
            "season",
            "projected_points",
            "replacement_points",
            "vorp",
        ]
    ].copy()

    available_players_projections_df.insert(0, "projection_id", range(1, len(available_players_projections_df) + 1))

    # start up database connection
    with duckdb.connect(DB_PATH) as con:
        schema_sql = SCHEMA_PATH.read_text()
        con.execute(schema_sql)

        con.register("available_players_df",  available_players_df)
        con.register("projections_df", available_players_projections_df)

        available_players_result = con.execute(
            """
            SELECT
                ap.player_name,
                ap.position,
                ap.nfl_team,
                fp.projected_points,
                fp.replacement_points,
                fp.vorp
            FROM dim_player ap
            JOIN fact_player_projection fp USING (player_id)
            LEFT JOIN fact_draft_pick fdp USING (player_id)
            WHERE fdp.player_id IS NULL
            ORDER BY fp.vorp DESC
            """
        ).fetchdf()

        # print available players result
        print("Available Players:")
        print(available_players_result)
        print("--------------------------------")

if __name__ == "__main__":
    load_sample_players()
    load_draft_picks()
    load_available_players()