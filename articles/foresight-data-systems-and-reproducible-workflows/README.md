# Foresight Data Systems and Reproducible Workflows

Professional companion repository directory for the Futures Thinking article **Foresight Data Systems and Reproducible Workflows**.

## Purpose

This directory operationalizes foresight data systems and reproducible workflows as practical futures-intelligence infrastructure. It includes synthetic drivers, signals, scenarios, assumptions, strategy evaluations, lineage records, workflow metadata, validation rules, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Structure

- `python/` — standard-library and optional advanced workflows for validation, traceability, quality scoring, assumption fragility, and reproducible reporting.
- `r/` — base R workflows for data quality, scenario traceability, and assumption review.
- `julia/`, `rust/`, `go/`, `cpp/`, `fortran/`, `c/` — small scoring examples for cross-language scaffolding.
- `sql/` — SQLite-compatible schema and analytical views.
- `docs/` — methodology, data dictionary, validation checklist, and reproducibility notes.
- `data/` — synthetic datasets.
- `outputs/` — generated tables and reports.
- `notebooks/` — notebook placeholders.

## Quick Start

```bash
bash run_smoke_tests.sh
```

The default Python workflow uses only the Python standard library.

Optional advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/foresight_data_systems_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/foresight-data-systems-and-reproducible-workflows/
