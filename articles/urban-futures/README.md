# Urban Futures

This is the professional companion repository directory for the Futures Thinking article:

**Urban Futures**

## Purpose

This directory operationalizes urban futures as a reproducible foresight and systems-analysis workflow. It includes synthetic urban system profiles, scenario records, strategy options, risk indicators, governance records, urban stress pathway simulations, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/urban-futures/`

## Structure

- `python/` — standard-library and optional advanced workflows for urban viability, fragility, scenario stress, strategy value, risk priority, governance capacity, and stress-path simulation.
- `r/` — base R workflows for comparing urban system profiles.
- `julia/` — urban viability scoring examples.
- `sql/` — schemas for urban profiles, scenarios, strategies, risk indicators, governance records, and pathways.
- `rust/` — command-line urban viability scoring scaffold.
- `go/` — urban futures utility scaffold.
- `cpp/` — efficient scoring examples.
- `fortran/` — numerical urban viability examples.
- `c/` — low-level scoring utility.
- `docs/` — methodology, data dictionary, validation checklist, and reproducibility notes.
- `data/` — synthetic datasets.
- `outputs/` — generated output tables and reports.
- `notebooks/` — notebook placeholders.

## Quick Start

Run the default smoke test:

```bash
bash run_smoke_tests.sh
```

The default Python workflow uses only the Python standard library.

Optional advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/urban_futures_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/urban-futures/
