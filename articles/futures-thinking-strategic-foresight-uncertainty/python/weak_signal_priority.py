"""
Futures Thinking: Weak Signal Priority Model

Educational example for scoring weak signals by novelty, uncertainty, potential impact,
and monitoring priority.
"""

from __future__ import annotations

import pandas as pd


def compute_signal_score(row: pd.Series) -> float:
    """Compute a stylized weak-signal priority score."""
    return (
        0.25 * row["novelty"]
        + 0.20 * row["uncertainty"]
        + 0.35 * row["potential_impact"]
        + 0.20 * row["monitoring_priority"]
    )


def main() -> None:
    signals = pd.read_csv("../data/weak_signals.csv")
    signals["signal_priority_score"] = signals.apply(compute_signal_score, axis=1)

    signals = signals.sort_values("signal_priority_score", ascending=False)

    print(signals)

    signals.to_csv("../outputs/weak_signal_priority_scores.csv", index=False)


if __name__ == "__main__":
    main()
