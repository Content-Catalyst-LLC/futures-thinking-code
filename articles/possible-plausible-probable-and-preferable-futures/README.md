# Possible, Plausible, Probable, and Preferable Futures

This is the professional companion repository directory for the Futures Thinking article:

**Possible, Plausible, Probable, and Preferable Futures**

## Purpose

This directory operationalizes the distinction between possible, plausible, probable, and preferable futures. It includes synthetic but realistic datasets, future-category classification, plausibility scoring, probability scoring, preference scoring, robust strategy fit, category-shift monitoring, SQL schemas, documentation, and multi-language computational examples.

## Directory

`articles/possible-plausible-probable-and-preferable-futures/`

## Structure

- `python/` — standard-library and optional advanced workflows for future-category classification.
- `r/` — base R workflows for category scoring and strategy-fit summaries.
- `julia/` — dynamic future-category scoring examples.
- `sql/` — schemas for candidate futures, drivers, scenarios, preference criteria, category shifts, and strategy fit.
- `rust/` — command-line category-scoring scaffold.
- `go/` — future-category utility scaffold.
- `cpp/` — efficient scoring example.
- `fortran/` — numerical category-scoring example.
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
python python/future_categories_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/possible-plausible-probable-and-preferable-futures/
