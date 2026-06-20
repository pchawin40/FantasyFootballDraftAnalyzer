# Create a local DuckDB database and load sample players
import duckdb
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "sample_players.csv"
DB_PATH = ROOT_DIR / "fantasy_football.duckdb"
SCHEMA_PATH = ROOT_DIR / "sql" / "01_schema.sql"

def load_sample_players():
    """
    load sample players from CSV file into DuckDB database
    """
    df = pd.read_csv(DATA_PATH)

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

        print(result)

if __name__ == "__main__":
    load_sample_players()