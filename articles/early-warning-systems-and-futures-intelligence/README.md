# Early Warning Systems and Futures Intelligence

This is the professional companion repository directory for the Futures Thinking article:

**Early Warning Systems and Futures Intelligence**

## Purpose

This directory operationalizes early warning systems and futures intelligence as a reproducible foresight workflow. It includes synthetic signal registers, warning indicators, threshold triggers, scenario monitors, assumption-failure tracking, cross-system cascade analysis, response protocols, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/early-warning-systems-and-futures-intelligence/`

## Structure

- `python/` — standard-library and optional advanced workflows for signal scoring, threshold triggers, assumption failure, scenario monitoring, and warning reports.
- `r/` — base R workflows for signal priority and warning-trigger scoring.
- `julia/` — warning-score examples.
- `sql/` — schemas for signals, indicators, thresholds, triggers, scenarios, assumptions, interactions, and response protocols.
- `rust/` — command-line early-warning diagnostics scaffold.
- `go/` — warning score utility scaffold.
- `cpp/` — efficient warning-score examples.
- `fortran/` — numerical early-warning examples.
- `c/` — low-level warning scoring utility.
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
python python/early_warning_futures_intelligence_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/early-warning-systems-and-futures-intelligence/
