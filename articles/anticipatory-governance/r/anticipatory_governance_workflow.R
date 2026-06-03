# Base R workflow for Anticipatory Governance.
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

profiles <- read.csv(file.path(data_dir, "governance_profiles.csv"))
signals <- read.csv(file.path(data_dir, "weak_signal_register.csv"))
scenarios <- read.csv(file.path(data_dir, "scenario_profiles.csv"))

profiles$anticipatory_capacity_score <- round(
  0.12 * profiles$detection_capacity +
  0.12 * profiles$interpretation_capacity +
  0.12 * profiles$scenario_capacity +
  0.12 * profiles$preparedness_capacity +
  0.12 * profiles$legitimacy +
  0.10 * profiles$coordination_capacity +
  0.10 * profiles$adaptive_authority +
  0.08 * profiles$equity_safeguards +
  0.07 * profiles$learning_capacity +
  0.05 * profiles$implementation_connection,
  4
)

profiles$anticipatory_fragility_pressure_score <- round(
  0.16 * (1 - profiles$detection_capacity) +
  0.14 * (1 - profiles$preparedness_capacity) +
  0.14 * (1 - profiles$adaptive_authority) +
  0.14 * (1 - profiles$coordination_capacity) +
  0.14 * (1 - profiles$legitimacy) +
  0.12 * (1 - profiles$equity_safeguards) +
  0.08 * (1 - profiles$learning_capacity) +
  0.08 * (1 - profiles$implementation_connection),
  4
)

profiles <- profiles[order(-profiles$anticipatory_capacity_score), ]

signals$weak_signal_priority_score <- round(
  0.16 * signals$signal_strength +
  0.14 * signals$novelty +
  0.12 * signals$uncertainty +
  0.18 * signals$system_relevance +
  0.16 * signals$justice_relevance +
  0.12 * signals$detection_difficulty +
  0.12 * (1 - signals$response_readiness),
  4
)

signals$response_gap_score <- round(1 - signals$response_readiness, 4)
signals <- signals[order(-signals$weak_signal_priority_score), ]

scenarios$future_stress_pressure_score <- round(
  0.16 * scenarios$technology_acceleration +
  0.18 * scenarios$climate_stress +
  0.14 * (1 - scenarios$public_trust) +
  0.14 * scenarios$geopolitical_volatility +
  0.12 * scenarios$fiscal_pressure +
  0.10 * (1 - scenarios$institutional_capacity) +
  0.08 * (1 - scenarios$participation_quality) +
  0.08 * scenarios$crisis_frequency,
  4
)

scenarios$democratic_anticipatory_opportunity_score <- round(
  0.22 * scenarios$institutional_capacity +
  0.22 * scenarios$participation_quality +
  0.20 * scenarios$public_trust +
  0.12 * (1 - scenarios$fiscal_pressure) +
  0.10 * (1 - scenarios$crisis_frequency) +
  0.08 * (1 - scenarios$geopolitical_volatility) +
  0.06 * (1 - scenarios$climate_stress),
  4
)

scenarios <- scenarios[order(-scenarios$future_stress_pressure_score), ]

write.csv(profiles, file.path(outputs_dir, "r_governance_profile_scores.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_weak_signal_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_scenario_profile_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_anticipatory_capacity_scores.png"), width = 1200, height = 800)
barplot(
  profiles$anticipatory_capacity_score,
  names.arg = profiles$governance_strategy,
  horiz = TRUE,
  las = 1,
  main = "Anticipatory Governance Capacity Scores",
  xlab = "Anticipatory capacity"
)
dev.off()

png(file.path(outputs_dir, "r_weak_signal_priority_scores.png"), width = 1200, height = 800)
barplot(
  signals$weak_signal_priority_score,
  names.arg = signals$signal_name,
  horiz = TRUE,
  las = 1,
  main = "Weak Signal Priority Scores",
  xlab = "Priority score"
)
dev.off()

print(profiles[, c("governance_id", "governance_strategy", "anticipatory_capacity_score", "anticipatory_fragility_pressure_score")])
print(signals[, c("signal_id", "signal_name", "weak_signal_priority_score", "response_gap_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
