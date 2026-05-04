"""
Futures Thinking: Scenario Matrix Generator

Educational example for creating a simple 2x2 scenario matrix from two uncertainties.
"""

from __future__ import annotations

import pandas as pd


def build_scenario_matrix(
    uncertainty_x: str = "Technology Governance",
    uncertainty_y: str = "Climate Stress"
) -> pd.DataFrame:
    scenarios = [
        {
            "scenario": "Coordinated Transition",
            uncertainty_x: "High coordination",
            uncertainty_y: "High stress",
            "interpretation": "Strong governance capacity responds to severe climate stress."
        },
        {
            "scenario": "Stable Adaptation",
            uncertainty_x: "High coordination",
            uncertainty_y: "Low stress",
            "interpretation": "Institutions adapt gradually under manageable stress."
        },
        {
            "scenario": "Fragmented Crisis",
            uncertainty_x: "Low coordination",
            uncertainty_y: "High stress",
            "interpretation": "Low coordination and severe stress produce systemic instability."
        },
        {
            "scenario": "Uneven Continuity",
            uncertainty_x: "Low coordination",
            uncertainty_y: "Low stress",
            "interpretation": "Stress remains manageable, but weak coordination preserves fragility."
        }
    ]

    return pd.DataFrame(scenarios)


def main() -> None:
    matrix = build_scenario_matrix()
    print(matrix)
    matrix.to_csv("../outputs/scenario_matrix.csv", index=False)


if __name__ == "__main__":
    main()
