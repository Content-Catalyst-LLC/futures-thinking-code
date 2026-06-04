# Migration, Demography, and Future Societies

This is the professional companion repository directory for the Futures Thinking article:

**Migration, Demography, and Future Societies**

## Purpose

This directory operationalizes migration, demography, and future societies as a reproducible demographic-stress, care-capacity, climate-mobility, labor-adaptation, housing-pressure, and social-cohesion workflow. It includes synthetic demographic profiles, migration scenarios, strategy options, risk indicators, urban/care records, adaptive pathway parameters, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/migration-demography-and-future-societies/`

## Structure

- `python/` — standard-library and optional advanced workflows for demographic stress, care stress, mobility pressure, adaptive capacity, strategy scoring, and population simulation.
- `r/` — base R workflows for comparing demographic futures and adaptation gaps.
- `julia/` — demographic stress scoring examples.
- `sql/` — schemas for demographic profiles, scenarios, strategies, risk indicators, urban/care records, and adaptive pathways.
- `rust/` — command-line demographic stress scoring scaffold.
- `go/` — demographic scoring utility scaffold.
- `cpp/` — efficient scoring examples.
- `fortran/` — numerical demographic-stress examples.
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
python python/migration_demography_future_societies_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/migration-demography-and-future-societies/
