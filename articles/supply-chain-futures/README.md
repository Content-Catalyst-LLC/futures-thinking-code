# Supply Chain Futures

This is the professional companion repository directory for the Futures Thinking article:

**Supply Chain Futures**

## Purpose

This directory operationalizes supply chain futures as a reproducible foresight and resilience workflow. It includes synthetic supply chain profiles, future scenarios, resilience strategies, chokepoint records, procurement and circularity records, disruption pathway simulations, SQL schemas, documentation, generated outputs, and multi-language computational examples.

## Directory

`articles/supply-chain-futures/`

## Structure

- `python/` — standard-library and optional advanced workflows for resilience scoring, fragility, chokepoints, strategy options, procurement, circularity, and disruption-pathway simulation.
- `r/` — base R workflows for comparing supply chain future profiles.
- `julia/` — supply chain resilience scoring examples.
- `sql/` — schemas for supply profiles, scenarios, strategies, chokepoints, procurement/circularity records, and disruption pathways.
- `rust/` — command-line supply chain resilience scoring scaffold.
- `go/` — supply chain futures utility scaffold.
- `cpp/` — efficient scoring examples.
- `fortran/` — numerical supply chain resilience examples.
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
python python/supply_chain_futures_advanced.py
```

## GitHub URL

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/supply-chain-futures/
