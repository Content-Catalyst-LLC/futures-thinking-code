# Methodology

This workflow scores technology readiness, governance gaps, distributional risks, signal priorities, pathway trajectories, and public-interest strategy options.

Core equations:

- Enabling score combines maturity, capability growth, support, infrastructure readiness, governance readiness, legitimacy, and inverse ecological pressure.
- Risk score combines distributional risk, ecological pressure, governance gap, legitimacy gap, and strategic importance.
- Foresight priority combines risk and enabling scores.
- Governance readiness combines regulatory capacity, standards maturity, accountability infrastructure, participation, and enforcement feasibility.
- Distributional risk combines burden concentration, exposure, worker displacement, community vulnerability, and inverse mitigation capacity.

Scores are structured prompts for judgment, not deterministic predictions.
## SQLite Compatibility Note

The pathway parameter field is named `constraint_pressure` rather than `constraint` because `CONSTRAINT` is a reserved SQL keyword. This keeps the SQLite smoke test and future data imports stable.

