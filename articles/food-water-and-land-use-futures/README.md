# Food, Water, and Land-Use Futures

This is the professional companion repository directory for the Futures Thinking article:

**Food, Water, and Land-Use Futures**

## Purpose

This directory operationalizes food, water, and land-use futures as a reproducible coupled resource-systems workflow. It includes synthetic food-water-land profiles, scenario records, strategy options, risk indicators, governance records, resource stress pathways, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/food-water-and-land-use-futures/`

## Structure

- `python/` — standard-library and optional advanced workflows for resilience, fragility, scenario stress, strategy value, risk priority, governance capacity, and resource-stress simulation.
- `r/` — base R workflows for comparing food-water-land system profiles.
- `julia/` — resilience scoring examples.
- `sql/` — schemas for profiles, scenarios, strategies, risk indicators, governance records, and pathways.
- `rust/` — command-line resilience scoring scaffold.
- `go/` — food-water-land futures utility scaffold.
- `cpp/` — efficient scoring examples.
- `fortran/` — numerical resilience examples.
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
python python/food_water_land_futures_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/food-water-and-land-use-futures/
