# Strategic Robustness Across Futures

This is the professional companion repository directory for the Futures Thinking article:

**Strategic Robustness Across Futures**

## Purpose

This directory operationalizes strategic robustness across futures as a reproducible foresight workflow. It includes synthetic scenario data, strategy portfolios, multi-criteria performance matrices, worst-case robustness scores, regret analysis, vulnerability diagnostics, adaptive triggers, assumption registers, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/strategic-robustness-across-futures/`

## Structure

- `python/` — standard-library and optional advanced workflows for robustness, regret, vulnerability, and adaptive triggers.
- `r/` — base R workflows for strategy robustness and regret scoring.
- `julia/` — robustness and viability scoring examples.
- `sql/` — schemas for scenarios, strategies, performance, regret, triggers, vulnerabilities, and assumptions.
- `rust/` — command-line robustness diagnostics scaffold.
- `go/` — strategy viability utility scaffold.
- `cpp/` — efficient robustness-score examples.
- `fortran/` — numerical worst-case viability examples.
- `c/` — low-level strategy scoring utility.
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
python python/strategic_robustness_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/strategic-robustness-across-futures/
