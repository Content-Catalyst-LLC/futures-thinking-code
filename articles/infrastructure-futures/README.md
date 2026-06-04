# Infrastructure Futures

This is the professional companion repository directory for the Futures Thinking article:

**Infrastructure Futures**

## Purpose

This directory operationalizes infrastructure futures as a reproducible systems-analysis workflow. It includes synthetic infrastructure system profiles, scenario records, strategy options, risk indicators, governance records, interdependent cascade pathways, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/infrastructure-futures/`

## Structure

- `python/` — standard-library and optional advanced workflows for infrastructure viability, fragility, scenario stress, strategy value, risk priority, governance capacity, and cascade-path simulation.
- `r/` — base R workflows for comparing infrastructure system profiles.
- `julia/` — infrastructure viability scoring examples.
- `sql/` — schemas for infrastructure profiles, scenarios, strategies, risk indicators, governance records, and pathways.
- `rust/` — command-line infrastructure viability scoring scaffold.
- `go/` — infrastructure futures utility scaffold.
- `cpp/` — efficient scoring examples.
- `fortran/` — numerical infrastructure viability examples.
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
python python/infrastructure_futures_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/infrastructure-futures/
