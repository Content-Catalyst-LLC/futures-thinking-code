# Economic Futures and Global Development

This is the professional companion repository directory for the Futures Thinking article:

**Economic Futures and Global Development**

## Purpose

This directory operationalizes economic futures and global development as a reproducible development-futures workflow. It includes synthetic development profiles, economic scenarios, policy portfolios, shock and stressor records, institutional capacity records, development pathway simulations, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/economic-futures-and-global-development/`

## Structure

- `python/` — standard-library and optional advanced workflows for development profiles, fragility, fiscal capacity, ecological stress, inequality, policy portfolios, and pathway simulation.
- `r/` — base R workflows for comparing economic futures profiles.
- `julia/` — development profile scoring examples.
- `sql/` — schemas for development profiles, scenarios, policies, stressors, institutions, and pathways.
- `rust/` — command-line development scoring scaffold.
- `go/` — economic futures utility scaffold.
- `cpp/` — efficient scoring examples.
- `fortran/` — numerical development profile examples.
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
python python/economic_futures_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/economic-futures-and-global-development/
