# import databases and libraries needed to run export recommendations
import duckdb
from pathlib import Path

# set root directory
ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "fantasy_football.duckdb"
VIEW_SQL_PATH = ROOT_DIR / "sql" / "08_create_recommendation_view.sql"
OUTPUT_PATH = ROOT_DIR / "outputs" / "draft_recommendations.csv"

def export_draft_recommendations():
    """
    export draft recommendations from DuckDB database
    """

    # 1. Connect to fantasy_football.duckdb database
    with duckdb.connect(DB_PATH) as con:
        # 2. Run sql/08_create_recommendation_view.sql
        view_sql_path = VIEW_SQL_PATH.read_text()
        con.execute(view_sql_path)

        # 3 Query SELECT * FROM recommendation_view
        result = con.execute(    
        """
        SELECT * FROM draft_recommendations
        """
        ).fetchdf()

        # 4 Save the result to outputs/draft_recommendations.csv
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(OUTPUT_PATH, index=False)
        print(f"Draft recommendations exported to {OUTPUT_PATH}")

if __name__ == "__main__":
    export_draft_recommendations()