# Fantasy Football Draft Analyzer
*By Chawin Pathompornvivat*

A portfolio analytics project that builds a fantasy football draft decision engine using Python, DuckDB, SQL, and Power BI. The project ranks available players in a 12-team half-PPR draft by combining value over replacement, position scarcity, current roster need, and recommendation reason.

**Table of Contents**
* [Getting Started](#getting-started)
* [Skills Demonstrated](#skills-demonstrated)
* [Fantasy Football Draft Analyzer at a Glance](#fantasy-football-draft-analyzer-at-a-glance)
* [Analytics Objective](#analytics-objective)
* [Data Pipeline and Technologies Used](#data-pipeline-and-technologies-used)
* [Real NFL Data Pipeline](#real-nfl-data-pipeline)
* [Data Model Overview](#data-model-overview)
* [SQL Analytics Workflow](#sql-analytics-workflow)
* [Dashboard Overview](#dashboard-overview)
* [Key Metrics](#key-metrics)
* [Project Structure](#project-structure)
* [Data Quality Checks](#data-quality-checks)
* [Common Commands](#common-commands)
* [Conclusion and Next Steps](#conclusion-and-next-steps)
* [Data Dictionary](docs/data_dictionary.md)

## Skills Demonstrated
- Built an end-to-end analytics pipeline using Python, pandas, DuckDB, and SQL
- Designed a star-schema-inspired data model for player projections and draft picks
- Created SQL logic for VORP, position scarcity, roster need, and recommendation scoring
- Added real NFL data using nflverse-derived player stats
- Built data quality checks for source files, transformed data, draft picks, and final outputs
- Wrote pytest tests for positive and negative validation cases
- Automated test execution with GitHub Actions
- Built a Power BI dashboard for draft-room decision support

## Getting Started

To run this project locally, clone the repository:

```bash
git clone https://github.com/pchawin40/FantasyFootballDraftAnalyzer.git
cd FantasyFootballDraftAnalyzer
```

### Create and Activate a Virtual Environment

Create the virtual environment one time:

```bash
python3 -m venv .venv
```

Activate it each time you work on the project:

```bash
source .venv/bin/activate
```

When the virtual environment is active, the terminal should show something similar to:

```bash
(.venv) ~/personal/FantasyFootballDraftAnalyzer$
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Run the Sample Data Pipeline

The original project pipeline can be run with one command:

```bash
python -m src.run_pipeline
```

This command:

1. Loads sample player projection data
2. Loads sample drafted-player data
3. Creates or refreshes the DuckDB database
4. Builds the recommendation SQL view
5. Exports the final dashboard-ready CSV to `outputs/draft_recommendations.csv`

The sample pipeline validates both the input files and final dashboard output before completion.

### Run the Real NFL Data Pipeline

I also added a real-data version using nflverse data. This is separate from the sample pipeline so the demo data still works while I keep building out the real workflow.

```bash
python -m src.run_real_data_pipeline
```

This command:

1. Pulls 2025 player stats from nflverse
2. Filters to fantasy positions only: QB, RB, WR, TE
3. Turns weekly stats into one season-level row per player
4. Uses historical fantasy points as a baseline projected points value
5. Adds replacement points by position
6. Loads the model-ready player data into DuckDB
7. Exports the final recommendation output

The processed real player file is saved here:

```text
data/processed/player_projections_2025.csv
```

The final recommendation output is still saved here:

```text
outputs/draft_recommendations.csv
```

### Run Tests

```bash
pytest
```

Expected result:

```text
all tests should pass
```

GitHub Actions also runs the test suite automatically on push and pull request.

## Fantasy Football Draft Analyzer at a Glance

Fantasy managers have to make draft decisions under uncertainty. A player may have strong projected points, but the best pick also depends on roster construction, remaining player pool, position scarcity, and replacement-level value.

The Fantasy Football Draft Analyzer simulates that decision process by ranking available players based on:

* Value over replacement player, or VORP
* Position scarcity
* Current roster need
* Final recommendation score
* Plain-English recommendation reason

The final output is designed for a draft-room dashboard where a user can quickly answer:

* Who is the best available player at my current pick?
* Which positions are becoming scarce?
* Does this player fit my current roster?
* Why is this player being recommended?

## Analytics Objective

### Research Question

Given my draft position, current roster, league scoring settings, and the players already selected, which available player provides the greatest incremental value for my team?

### Project Objective

Build an end-to-end analytics workflow that transforms player and draft data into an explainable draft recommendation system. The project demonstrates skills for data modeling, SQL analytics, pipeline design, metric development, and dashboard reporting.

## Data Pipeline and Technologies Used

This project uses a lightweight local analytics stack:

* **Python**: Loads sample data, pulls real NFL data, refreshes the pipeline, and exports dashboard-ready output
* **Pandas**: Handles CSV-based data transformations
* **DuckDB**: Serves as the local analytical database
* **SQL**: Builds schemas, views, player rankings, and recommendation logic
* **Power BI Desktop**: Creates the Draft Command Center dashboard
* **Pytest**: Validates scoring, value calculations, and quality checks
* **GitHub Actions**: Runs tests automatically on push and pull request
* **GitHub**: Stores project code, documentation, and dashboard artifacts

### Sample Pipeline Flow

```text
sample_players.csv
        |
        v
Python load script
        |
        v
DuckDB tables
        |
        v
SQL recommendation view
        |
        v
draft_recommendations.csv
        |
        v
Power BI dashboard
```

### Real Data Pipeline Flow

```text
nflverse player stats
        |
        v
extract_nflverse.py
        |
        v
raw player stats CSV
        |
        v
transform_nflverse.py
        |
        v
player_projections_2025.csv
        |
        v
load_real_data.py
        |
        v
DuckDB tables
        |
        v
SQL recommendation view
        |
        v
draft_recommendations.csv
```

## Real NFL Data Pipeline

The first version of this project used sample data because I wanted the scoring, SQL logic, and dashboard to work first before adding messier real data.

After that was working, I added a real-data pipeline using nflverse player stats. The goal is not to make a perfect fantasy projection model yet. Right now the real-data workflow uses prior-season fantasy points as a simple baseline projection so the rest of the draft analyzer can run with real NFL player data.

The real-data scripts are:

* `src/extract_nflverse.py`: pulls player stats from nflverse and saves raw CSV files
* `src/transform_nflverse.py`: filters QB/RB/WR/TE and creates a model-ready player projection file
* `src/load_real_data.py`: loads the real projection file into the same DuckDB tables used by the sample pipeline
* `src/run_real_data_pipeline.py`: runs the full real-data workflow

The real projection file has the same main structure as the sample player file:

```text
player_id
player_name
position
nfl_team
projected_points
replacement_points
```

That part is important because it lets the same SQL recommendation logic work for both the sample version and the real-data version.

## Data Model Overview

The current database uses a small star-schema-inspired model:

### `dim_player`

Stores player-level attributes.

```text
player_id
player_name
position
nfl_team
```

### `fact_player_projection`

Stores player projection and value metrics.

```text
projection_id
player_id
season
projected_points
replacement_points
vorp
```

### `fact_draft_pick`

Stores drafted players by pick and team.

```text
draft_pick_id
round_number
pick_number
team_number
player_id
```

This structure keeps player attributes, projections, and draft activity separate so the recommendation logic can be updated without rebuilding the entire project.

For detailed field definitions and metric logic, see the [Data Dictionary](docs/data_dictionary.md).

## SQL Analytics Workflow

The SQL workflow builds from simple player rankings into a recommendation model.

### 1. Player Value Ranking

`sql/03_player_value.sql` ranks players by projected value over replacement.

### 2. Available Player Filtering

`sql/04_available_players.sql` excludes players who already appear in the draft pick table.

### 3. Position Scarcity Score

`sql/05_recommendation_score.sql` calculates the number of available players by position and adds a scarcity adjustment.

### 4. Roster Need Adjustment

`sql/06_roster_need_score.sql` adjusts recommendations based on the current team's roster construction.

### 5. Recommendation Reason

`sql/07_recommendation_reason.sql` creates a plain-English reason for each recommendation, such as:

```text
High VORP + scarce position + roster need
High VORP + roster need
Scarce position
Depth option
```

### 6. Recommendation View

`sql/08_create_recommendation_view.sql` creates the final reusable recommendation view used by the export script and Power BI dashboard.

## Dashboard Overview

The Power BI dashboard, named **Draft Command Center**, presents the recommendation output in a presentable BI format.

![Draft Command Center](images/draft_command_center.png)

The dashboard includes:

* Top recommended player card
* Top recommendation score card
* Position slicer
* Recommendation score by player bar chart
* Detail table with player, position, VORP, recommendation score, and recommendation reason

The dashboard is powered by:

```text
outputs/draft_recommendations.csv
```

## Key Metrics

### Value Over Replacement Player, or VORP

VORP estimates how much more valuable a player is compared with a replacement-level option at the same position.

```text
VORP = projected_points - replacement_points
```

### Scarcity Adjustment

The scarcity adjustment gives a small boost to positions with fewer available players remaining.

```text
scarcity_adjustment = 10.0 / available_player_count
```

### Roster Need Adjustment

The roster need adjustment gives a boost to positions the current team has not filled yet.

```text
0 players at position = +8
1 player at position  = +4
2+ players at position = +0
```

### Recommendation Score

The final recommendation score combines the major decision factors.

```text
recommendation_score = VORP + scarcity_adjustment + roster_need_adjustment
```

## Project Structure

```text
.
├── README.md
├── .github/
│   └── workflows/
│       └── tests.yml
├── config/
│   └── league_settings.yaml
├── dashboard/
├── data/
│   ├── raw/
│   │   ├── player_stats_2025.csv
│   │   └── player_stats_2025_fantasy_positions.csv
│   ├── processed/
│   │   └── player_projections_2025.csv
│   ├── sample_draft_picks.csv
│   └── sample_players.csv
├── docs/
│   └── data_dictionary.md
├── images/
│   └── draft_command_center.png
├── outputs/
│   └── draft_recommendations.csv
├── requirements.txt
├── sql/
│   ├── 01_schema.sql
│   ├── 02_cleaning.sql
│   ├── 03_player_value.sql
│   ├── 04_available_players.sql
│   ├── 05_recommendation_score.sql
│   ├── 06_roster_need_score.sql
│   ├── 07_recommendation_reason.sql
│   └── 08_create_recommendation_view.sql
├── src/
│   ├── export_recommendations.py
│   ├── extract_nflverse.py
│   ├── load.py
│   ├── load_real_data.py
│   ├── quality_checks.py
│   ├── run_pipeline.py
│   ├── run_real_data_pipeline.py
│   └── transform_nflverse.py
└── tests/
    ├── test_quality_checks.py
    └── test_scoring.py
```

## Data Quality Checks

Input validation:
- Duplicate player IDs
- Missing player names
- Missing positions
- Negative projected/replacement points
- Drafted player IDs must exist in player pool
- Duplicate drafted player IDs

Real player projection validation:
- Real projection file exists
- File is not empty
- Required columns exist
- Player IDs are not missing
- Player IDs are not duplicated
- Player names are not missing
- Positions are only QB, RB, WR, TE
- Projected points are not missing or negative
- Replacement points are not missing or negative

Output validation:
- Recommendation output file exists
- Output is not empty
- Required dashboard columns exist
- Recommendation scores are not missing
- Recommendations scores are non-negative
- Player names are not missing
- Drafted players do not appear in recommendation output

## Common Commands

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the sample-data pipeline:

```bash
python -m src.run_pipeline
```

Run the real NFL data pipeline:

```bash
python -m src.run_real_data_pipeline
```

Run tests:

```bash
pytest
```

Open the DuckDB database:

```bash
duckdb fantasy_football.duckdb
```

Run a SQL file manually inside DuckDB:

```sql
.read sql/08_create_recommendation_view.sql
SELECT * FROM draft_recommendations;
```

Exit DuckDB:

```sql
.exit
```

## Conclusion and Next Steps

This project started as a fantasy football draft helper and developed into a small analytics decision engine. It demonstrates how raw player and draft data can be converted into a structured data model, analytical metrics, recommendation logic, and a BI dashboard.

The current version has two workflows: a stable sample-data pipeline and a real NFL data pipeline using nflverse player stats. The real-data version is still simple on purpose. It uses prior-season fantasy points as a baseline projection so I can keep the focus on data modeling, SQL logic, pipeline design, and dashboard output first.

Next improvements are:

* Add larger simulated drafted scenarios using nflverse player IDs
* Add more realistic replacement-level calculations by position
* Add bye week and risk indicators
* Add draft round and pick context
* Add model validation or backtesting against historical results
* Improve the Power BI dashboard layout and formatting
* Explore live draft data through Sleeper API or Yahoo Fantasy API later

The long-term goal is to turn this into a more realistic fantasy draft decision-support system while keeping the project relevant to analytics through clear data modeling, reproducible SQL logic, and business-style dashboard reporting.
