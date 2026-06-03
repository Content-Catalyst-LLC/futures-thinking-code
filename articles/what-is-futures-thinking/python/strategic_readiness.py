"""
Futures Thinking: Strategic Readiness Across Multiple Futures

Educational model comparing strategy performance under multiple plausible futures.
"""

from __future__ import annotations

import pandas as pd


def summarize_strategy_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize performance and robustness across futures."""
    summary = (
        df.groupby("strategy")["performance"]
        .agg(
            mean_performance="mean",
            worst_case="min",
            best_case="max",
            performance_range=lambda x: x.max() - x.min()
        )
        .reset_index()
    )

    summary["robustness_score"] = (
        0.50 * summary["worst_case"]
        + 0.30 * summary["mean_performance"]
        - 0.20 * summary["performance_range"]
    )

    return summary.sort_values("robustness_score", ascending=False)


def main() -> None:
    df = pd.read_csv("../data/strategy_future_performance.csv")
    summary = summarize_strategy_performance(df)

    print("Scenario performance:")
    print(df.head())

    print("\nStrategy robustness summary:")
    print(summary)

    df.to_csv("../outputs/strategy_future_performance.csv", index=False)
    summary.to_csv("../outputs/strategy_readiness_summary.csv", index=False)


if __name__ == "__main__":
    main()
