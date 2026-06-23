# Load real draft picks into DuckDB fact_draft_pick table

import duckdb
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
REAL_DRAFT_PICKS_PATH = ROOT_DIR / "data" / "real_draft_picks_2025.csv"
DB_PATH = ROOT_DIR / "fantasy_football.duckdb"
SCHEMA_PATH = ROOT_DIR / "sql" / "01_schema.sql"

def load_real_draft_picks():
    """
    Load real draft picks from data/real_draft_picks_2025.csv into fact_draft_pick
    """
    print ("Loading real draft picks...")

    # 1. Read real draft picks CSV
    df = pd.read_csv(REAL_DRAFT_PICKS_PATH)

    # 2. Keep only the columns needed by fact_draft_pick
    draft_picks_df = df[
        [
            "round_number",
            "pick_number",
            "team_number",
            "player_id",
        ]
    ].copy()

    # 3. Add draft_pick_id
    draft_picks_df.insert(
        0,
        "draft_pick_id",
        range(1, len(draft_picks_df) + 1)
    )

    # 4. Load into DuckDB
    with duckdb.connect(DB_PATH) as con:
        schema_sql = SCHEMA_PATH.read_text()
        con.execute(schema_sql)

        # Clear existing draft picks to avoid duplicate inserts
        con.execute("DELETE FROM fact_draft_pick")

        con.register("draft_picks_df", draft_picks_df)

        con.execute(
            "INSERT INTO fact_draft_pick SELECT * FROM draft_picks_df"
        )

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

        print("Real Draft Picks Result: ")
        print(draft_picks_result)
        print("--------------------")

if __name__ == "__main__":
    load_real_draft_picks()