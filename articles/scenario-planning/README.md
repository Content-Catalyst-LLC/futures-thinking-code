# Scenario Planning

This is the professional companion repository directory for the Futures Thinking article:

**Scenario Planning**

## Purpose

This directory operationalizes scenario planning through reproducible examples. It includes synthetic but realistic scenario datasets, critical uncertainty scoring, strategy robustness analysis, regret analysis, signal monitoring, assumption vulnerability scoring, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/scenario-planning/`

## Structure

- `python/` — standard-library and optional advanced workflows for scenario planning analysis.
- `r/` — base R workflows for scenario strategy profiles and robustness summaries.
- `julia/` — dynamic scenario robustness examples.
- `sql/` — schemas for scenarios, drivers, uncertainties, signals, assumptions, strategies, and evaluations.
- `rust/` — command-line scenario diagnostics scaffold.
- `go/` — scenario and strategy scoring utility scaffold.
- `cpp/` — efficient robustness scoring example.
- `fortran/` — numerical scenario-readiness example.
- `c/` — low-level scenario scoring utility.
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
python python/scenario_planning_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/scenario-planning/
