# Delphi Method and Expert Foresight

This is the professional companion repository directory for the Futures Thinking article:

**Delphi Method and Expert Foresight**

## Purpose

This directory operationalizes Delphi and expert foresight as a reproducible research workflow. It includes synthetic but realistic expert-panel data, round-by-round judgment records, consensus and dissensus metrics, uncertainty-range analysis, expert-selection audits, qualitative theme summaries, priority scoring, scenario/policy translation tables, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/delphi-method-and-expert-foresight/`

## Structure

- `python/` — standard-library and optional advanced workflows for Delphi round analysis.
- `r/` — base R workflows for consensus, stability, and disagreement summaries.
- `julia/` — dynamic Delphi convergence examples.
- `sql/` — schemas for experts, rounds, responses, consensus metrics, rationales, themes, and foresight outputs.
- `rust/` — command-line Delphi diagnostics scaffold.
- `go/` — Delphi priority-score utility scaffold.
- `cpp/` — efficient consensus and dispersion examples.
- `fortran/` — numerical convergence examples.
- `c/` — low-level Delphi scoring utility.
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
python python/delphi_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/delphi-method-and-expert-foresight/
