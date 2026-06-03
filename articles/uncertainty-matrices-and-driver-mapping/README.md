# Uncertainty Matrices and Driver Mapping

This is the professional companion repository directory for the Futures Thinking article:

**Uncertainty Matrices and Driver Mapping**

## Purpose

This directory operationalizes uncertainty matrices and driver mapping as a reproducible foresight workflow. It includes synthetic but realistic driver registers, signal registers, impact-uncertainty scoring, interaction matrices, scenario-axis selection, monitoring indicators, assumption-failure triggers, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/uncertainty-matrices-and-driver-mapping/`

## Structure

- `python/` — standard-library and optional advanced workflows for driver scoring, uncertainty classification, interaction mapping, scenario-axis selection, and monitoring.
- `r/` — base R workflows for driver priority and uncertainty matrix classification.
- `julia/` — driver priority examples.
- `sql/` — schemas for drivers, interactions, signals, monitoring indicators, and assumptions.
- `rust/` — command-line driver diagnostics scaffold.
- `go/` — uncertainty-priority utility scaffold.
- `cpp/` — efficient driver-priority examples.
- `fortran/` — numerical uncertainty-matrix examples.
- `c/` — low-level driver scoring utility.
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
python python/uncertainty_driver_mapping_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/uncertainty-matrices-and-driver-mapping/
