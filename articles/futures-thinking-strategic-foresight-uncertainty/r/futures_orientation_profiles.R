# Futures Thinking: Orientation Profiles in R
# Educational example only.

library(tidyverse)

orientations <- read_csv("../data/futures_orientations.csv", show_col_types = FALSE)

orientations <- orientations |>
  mutate(
    futures_profile =
      0.16 * uncertainty_tolerance +
      0.14 * assumption_visibility +
      0.15 * flexibility +
      0.16 * scenario_breadth +
      0.16 * long_horizon_readiness +
      0.12 * weak_signal_literacy +
      0.11 * governance_learning
  )

orientations_long <- orientations |>
  pivot_longer(
    cols = c(
      uncertainty_tolerance,
      assumption_visibility,
      flexibility,
      scenario_breadth,
      long_horizon_readiness,
      weak_signal_literacy,
      governance_learning
    ),
    names_to = "dimension",
    values_to = "value"
  )

planning_risk_flags <- orientations |>
  mutate(
    low_scenario_breadth = scenario_breadth < 0.60,
    low_assumption_visibility = assumption_visibility < 0.60,
    low_long_horizon_readiness = long_horizon_readiness < 0.60,
    planning_risk_flag =
      low_scenario_breadth | low_assumption_visibility | low_long_horizon_readiness
  )

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(orientations, "../outputs/r_futures_orientation_profiles.csv")
write_csv(orientations_long, "../outputs/r_futures_dimensions_long.csv")
write_csv(planning_risk_flags, "../outputs/r_planning_risk_flags.csv")

print(orientations)
print(planning_risk_flags)
