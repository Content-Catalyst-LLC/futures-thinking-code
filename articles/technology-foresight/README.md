# Technology Foresight

Professional companion repository directory for **Technology Foresight**.

## Purpose

This directory operationalizes technology foresight as a reproducible futures workflow. It includes synthetic technology profiles, readiness matrices, signal registers, scenario conditions, governance and distributional risk scores, pathway simulations, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Structure

- `python/` — standard-library and optional advanced workflows for readiness, governance, distributional risk, pathway simulation, and reports.
- `r/` — base R workflows for technology foresight profiles and readiness comparison.
- `julia/`, `rust/`, `go/`, `cpp/`, `fortran/`, `c/` — compact cross-language scoring examples.
- `sql/` — schemas for technologies, signals, scenarios, risks, governance controls, and strategy options.
- `docs/`, `data/`, `outputs/`, `notebooks/` — documentation, synthetic data, generated outputs, and notebook placeholders.

## Quick Start

```bash
bash run_smoke_tests.sh
```

Optional advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/technology_foresight_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/technology-foresight/
