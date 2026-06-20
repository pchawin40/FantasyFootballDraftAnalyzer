# Fantasy Football Draft Analyzer

## Brief Overview
The Fantasy Football Draft Analyzer is a data-driven decision tool designed to help fantasy football managers evaluate draft picks in a 12-team, half-PPR league format. The project analyzes player performance, positional scarcity, roster needs, and current draft availability to recommend which available players provide the most incremental value at each pick.

The goal is to simulate a real draft-room decision process using historical NFL performance data, fantasy scoring rules, and live or near-live draft data. Instead of only ranking players by projected points, the analyzer evaluates each player in the context of the manager's current roster, draft position, remaining player pool, and replacement-level value by position

## Research Question
Given my draft position, current roster, league scoring settings, and the players already selected, which available player provides the greatest incremental value for my team?

## Project Objective
Build an end-to-end analytic workflow that collects fantasy football and NFL performance data, transforms it into a structured data model, calculates player value metrics, and presents draft recommendations through SQL queries and a BI dashboard.

The final output should help answer:
• Who is the best available player at my current pick?
• Which position has the most scarcity at this stage of the draft?
• How much value does this player add compared with a replacement-level option?
• Is the recommended pick based on projected points, roster need, or positional advantage?