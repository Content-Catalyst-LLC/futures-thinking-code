# Base R workflow for Energy Transition Futures.
# No external packages required.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("--file=", "", file_arg))
  root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  root <- normalizePath(".", mustWork = TRUE)
}

data_dir <- file.path(root, "data")
outputs_dir <- file.path(root, "outputs")
dir.create(outputs_dir, showWarnings = FALSE, recursive = TRUE)

capabilities <- read.csv(file.path(data_dir, "energy_transition_capabilities.csv"))
scenarios <- read.csv(file.path(data_dir, "energy_transition_scenarios.csv"))
justice <- read.csv(file.path(data_dir, "justice_indicators.csv"))

score_readiness <- function(clean, grid, storage, electrification, phase_down, justice, labor, materials, resilience) {
  0.14 * clean + 0.14 * grid + 0.12 * storage + 0.12 * electrification +
    0.12 * phase_down + 0.12 * justice + 0.10 * labor + 0.08 * materials + 0.06 * resilience
}

score_risk <- function(grid, storage, phase_down, justice, labor, materials, resilience) {
  0.18 * (1 - grid) + 0.16 * (1 - storage) + 0.16 * (1 - phase_down) +
    0.14 * (1 - justice) + 0.12 * (1 - labor) + 0.12 * (1 - materials) + 0.12 * (1 - resilience)
}

capabilities$transition_readiness_score <- round(score_readiness(
  capabilities$clean_power_expansion,
  capabilities$grid_readiness,
  capabilities$storage_flexibility,
  capabilities$electrification_capacity,
  capabilities$fossil_phase_down,
  capabilities$energy_justice,
  capabilities$labor_transition,
  capabilities$material_responsibility,
  capabilities$climate_resilience
), 4)

capabilities$transition_risk_pressure_score <- round(score_risk(
  capabilities$grid_readiness,
  capabilities$storage_flexibility,
  capabilities$fossil_phase_down,
  capabilities$energy_justice,
  capabilities$labor_transition,
  capabilities$material_responsibility,
  capabilities$climate_resilience
), 4)

capabilities <- capabilities[order(-capabilities$transition_readiness_score), ]

scenarios$transition_readiness_score <- round(score_readiness(
  scenarios$clean_power_expansion,
  scenarios$grid_readiness,
  scenarios$storage_flexibility,
  scenarios$electrification_capacity,
  scenarios$fossil_phase_down,
  scenarios$energy_justice,
  scenarios$labor_transition,
  scenarios$material_responsibility,
  scenarios$climate_resilience
), 4)

scenarios$transition_risk_pressure_score <- round(score_risk(
  scenarios$grid_readiness,
  scenarios$storage_flexibility,
  scenarios$fossil_phase_down,
  scenarios$energy_justice,
  scenarios$labor_transition,
  scenarios$material_responsibility,
  scenarios$climate_resilience
), 4)

scenarios <- scenarios[order(-scenarios$transition_readiness_score), ]

justice$energy_justice_score <- round(
  0.18 * justice$affordability +
  0.16 * justice$community_voice +
  0.16 * justice$worker_security +
  0.16 * justice$health_benefit +
  0.12 * justice$ownership_access +
  0.12 * justice$repair_capacity +
  0.10 * justice$harm_reduction,
  4
)

justice$energy_justice_gap_score <- round(1 - justice$energy_justice_score, 4)
justice <- justice[order(-justice$energy_justice_score), ]

write.csv(capabilities, file.path(outputs_dir, "r_energy_transition_capability_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_energy_transition_scenario_scores.csv"), row.names = FALSE)
write.csv(justice, file.path(outputs_dir, "r_energy_justice_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_transition_readiness_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$transition_readiness_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Transition Readiness by Scenario",
  xlab = "Transition readiness"
)
dev.off()

png(file.path(outputs_dir, "r_transition_risk_pressure_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$transition_risk_pressure_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Transition Risk Pressure by Scenario",
  xlab = "Transition risk pressure"
)
dev.off()

print(scenarios[, c("scenario_id", "scenario_name", "transition_readiness_score", "transition_risk_pressure_score")])
print(capabilities[, c("capability_id", "capability_name", "transition_readiness_score", "transition_risk_pressure_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
