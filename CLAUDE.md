# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Analysis of the Stack Overflow Annual Developer Survey to identify which tech stacks maximize **salary, satisfaction, and employability** for a data/AI junior profile in Spain or remote Europe. Built as a portfolio piece with a concrete thesis, not a generic EDA.

## Setup

Requires [uv](https://github.com/astral-sh/uv).

```bash
uv sync                  # install dependencies
uv run jupyter notebook  # launch Jupyter for notebook work
uv run python src/lector.py  # run a script directly
```

## Data Pipeline

```
data/raw/results.csv  →  pandas (clean/normalize)  →  DuckDB (SQL queries)  →  pandas  →  seaborn/matplotlib  →  narrated notebook
```

- `data/raw/results.csv` — raw Stack Overflow survey CSV (not versioned, must be placed manually)
- `data/raw/schema.csv` — survey schema/column definitions
- `data/processed/` — outputs from the cleaning pipeline

## Architecture

- `src/` — reusable Python modules (cleaning, DuckDB connection, visualization helpers)
- `notebooks/` — narrated analysis (not yet created; will consume `src/` modules)
- `src/lector.py` — current entry point: filters survey to EU data/AI roles and explores salary and language columns

## Key Domain Concepts

**Target population filter** (defined in `src/lector.py`):
- Roles: Data engineer, AI/ML engineer, Data scientist, Data/business analyst, Applied scientist, Developer AI apps — plus DevOps/Cloud as adjacent roles
- Geography: 27 EU member states
- Salary column: `ConvertedCompYearly` (USD, pre-converted by SO)

## Dependencies

Managed via `uv` / `pyproject.toml`. Python ≥ 3.13 required.

- `pandas` — ingestion, cleaning, normalization
- `duckdb` — embedded SQL engine for metrics and window functions
- `matplotlib` + `seaborn` — visualization
- `jupyter` (dev) — analysis environment
