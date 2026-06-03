# Causal Layered Analysis

This is the professional companion repository directory for the Futures Thinking article:

**Causal Layered Analysis**

## Purpose

This directory operationalizes Causal Layered Analysis as a reproducible futures workflow. It includes synthetic but realistic CLA issue registers, layer-coded statements, worldview and metaphor maps, reframing profiles, power and legitimacy audits, scenario translation tables, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/causal-layered-analysis/`

## Structure

- `python/` — standard-library and optional advanced workflows for CLA layer and reframing analysis.
- `r/` — base R workflows for layer profiles, reframing depth, and power-aware summaries.
- `julia/` — dynamic CLA depth examples.
- `sql/` — schemas for issues, layer codes, metaphors, reframing profiles, power audits, and scenario translation.
- `rust/` — command-line CLA diagnostics scaffold.
- `go/` — CLA depth-score utility scaffold.
- `cpp/` — efficient reframing-depth examples.
- `fortran/` — numerical layered-analysis examples.
- `c/` — low-level CLA scoring utility.
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
python python/cla_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/causal-layered-analysis/
