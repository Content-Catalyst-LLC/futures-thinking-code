# Climate Futures and Environmental Change

This is the professional companion repository directory for the Futures Thinking article:

**Climate Futures and Environmental Change**

## Purpose

This directory operationalizes climate futures and environmental change as a reproducible climate-foresight workflow. It includes synthetic climate future profiles, scenario records, mitigation/adaptation strategies, climate risk indicators, governance records, climate pathway simulations, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/climate-futures-and-environmental-change/`

## Structure

- `python/` — standard-library and optional advanced workflows for climate readiness, fragility, risk priority, mitigation/adaptation strategy scoring, governance capacity, and climate pathway simulation.
- `r/` — base R workflows for comparing climate future profiles.
- `julia/` — climate readiness scoring examples.
- `sql/` — schemas for climate profiles, scenarios, strategies, risk indicators, governance records, and climate pathways.
- `rust/` — command-line climate readiness scoring scaffold.
- `go/` — climate futures utility scaffold.
- `cpp/` — efficient scoring examples.
- `fortran/` — numerical climate readiness examples.
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
python python/climate_futures_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/climate-futures-and-environmental-change/
