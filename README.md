# Fantasy Football Draft Analyzer

## Brief Overview

The Fantasy Football Draft Analyzer is a data-driven decision tool designed to help fantasy football managers evaluate draft picks in a 12-team, half-PPR league format. The project analyzes player performance, positional scarcity, roster needs, and current draft availability to recommend which available players provide the most incremental value at each pick.

The goal is to simulate a real draft-room decision process using historical NFL performance data, fantasy scoring rules, and live or near-live draft data. Instead of only ranking players by projected points, the analyzer evaluates each player in the context of the manager's current roster, draft position, remaining player pool, and replacement-level value by position.

## Research Question

Given my draft position, current roster, league scoring settings, and the players already selected, which available player provides the greatest incremental value for my team?

## Project Objective

Build an end-to-end analytics workflow that collects fantasy football and NFL performance data, transforms it into a structured data model, calculates player value metrics, and presents draft recommendations through SQL queries and a BI dashboard.

The final output should help answer:

- Who is the best available player at my current pick?
- Which position has the most scarcity at this stage of the draft?
- How much value does this player add compared with a replacement-level option?
- Is the recommended pick based on projected points, roster need, or positional advantage?

## Setup Instructions

Run these commands from the project root folder:

```bash
cd ~/personal/FantasyFootballDraftAnalyzer
```

### 1. Create a virtual environment

Only do this the first time you set up the project:

```bash
python3 -m venv .venv
```

### 2. Turn on the virtual environment

Run this every time you start working on the project:

```bash
source .venv/bin/activate
```

When the virtual environment is active, the terminal should show something like this:

```bash
(.venv) ~/personal/FantasyFootballDraftAnalyzer$
```

### 3. Install project packages

Run this after creating or activating the virtual environment:

```bash
pip install -r requirements.txt
```

## How to Run the Project

### 1. Run the Python loading script

This creates or refreshes the local DuckDB database and loads the sample player data:

```bash
python src/load.py
```

Expected result: the terminal should print a ranked table of players ordered by VORP.

### 2. Open the DuckDB database

```bash
duckdb fantasy_football.duckdb
```

### 3. Run the available-player SQL query

Inside DuckDB, run:

```sql
.read sql/04_available_players.sql
```

Expected result: drafted players should be excluded from the ranking, and only available players should appear.

### 4. Exit DuckDB

Inside DuckDB, run:

```sql
.exit
```

## How to Run Tests

Run this from the project root folder:

```bash
pytest
```

Expected result:

```text
2 passed
```

## Common Commands

### Turn on virtual environment

```bash
source .venv/bin/activate
```

### Turn off virtual environment

```bash
deactivate
```

### Run the data load script

```bash
python src/load.py
```

### Open DuckDB

```bash
duckdb fantasy_football.duckdb
```

### Run tests

```bash
pytest
```