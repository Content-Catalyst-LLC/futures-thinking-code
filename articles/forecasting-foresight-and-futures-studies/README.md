# Forecasting, Foresight, and Futures Studies

This article companion directory supports the Futures Thinking article:

**Forecasting, Foresight, and Futures Studies**

The workflows compare forecasting, strategic foresight, and futures studies as distinct but related practices. Forecasting emphasizes estimation, forecast error, and model evaluation. Foresight emphasizes scenario robustness, uncertainty, assumption visibility, strategic readiness, and regret analysis. Futures studies examines how futures are imagined, contested, governed, and shaped.

## Directory Structure

- `python/` — standard-library and optional advanced workflows for forecast error, scenario robustness, regret analysis, and strategy comparison.
- `r/` — base R workflow for comparing future-oriented practices.
- `julia/` — dynamic uncertainty and robustness examples.
- `sql/` — schema for forecasts, drivers, scenarios, assumptions, strategies, and evaluation outputs.
- `rust/` — command-line futures diagnostics scaffold.
- `go/` — scenario and forecast utility scaffold.
- `cpp/` — efficient strategy-performance and regret example.
- `fortran/` — numerical robustness example.
- `c/` — low-level scenario scoring utility.
- `docs/` — modeling notes, assumptions, and reproducibility guidance.
- `data/` — synthetic datasets.
- `outputs/` — generated output tables and summaries.
- `notebooks/` — notebook placeholders.

## Quick Start

From this directory:

```bash
bash run_smoke_tests.sh
```

The default Python workflow uses only the Python standard library.

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/forecasting_foresight_advanced.py
```

## Article Link

Repository article directory:

https://github.com/Content-Catalyst-LLC/futures-thinking-code/tree/main/articles/forecasting-foresight-and-futures-studies/
