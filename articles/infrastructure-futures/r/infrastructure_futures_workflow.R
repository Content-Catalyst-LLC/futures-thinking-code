# Base R workflow for Infrastructure Futures.
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

profiles <- read.csv(file.path(data_dir, "infrastructure_system_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "infrastructure_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "infrastructure_risk_indicators.csv"))

profiles$infrastructure_viability_score <- round(
  0.14 * (1 - profiles$centralization) +
  0.18 * profiles$redundancy -
  0.12 * profiles$digital_dependence -
  0.16 * profiles$climate_exposure +
  0.16 * profiles$coordination_quality +
  0.12 * profiles$public_finance_capacity +
  0.12 * profiles$maintenance_integrity +
  0.10 * profiles$equity_of_access -
  0.08 * profiles$geopolitical_dependency,
  4
)

profiles$infrastructure_fragility_score <- round(
  0.14 * profiles$centralization +
  0.14 * (1 - profiles$redundancy) +
  0.12 * profiles$digital_dependence +
  0.17 * profiles$climate_exposure +
  0.13 * (1 - profiles$coordination_quality) +
  0.11 * (1 - profiles$public_finance_capacity) +
  0.10 * (1 - profiles$maintenance_integrity) +
  0.08 * (1 - profiles$equity_of_access) +
  0.11 * profiles$geopolitical_dependency,
  4
)

profiles <- profiles[order(-profiles$infrastructure_viability_score), ]

strategies$infrastructure_strategy_value_score <- round(
  0.16 * strategies$redundancy_gain +
  0.16 * strategies$maintenance_gain +
  0.14 * strategies$climate_adaptation_gain +
  0.12 * strategies$digital_accountability_gain +
  0.14 * strategies$governance_gain +
  0.12 * strategies$finance_capacity_gain +
  0.12 * strategies$equity_gain +
  0.04 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$infrastructure_strategy_value_score), ]

risks$infrastructure_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$cascade_potential +
  0.12 * risks$visibility_gap +
  0.14 * risks$recovery_difficulty +
  0.17 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$infrastructure_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_infrastructure_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_infrastructure_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_infrastructure_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_infrastructure_viability_scores.png"), width = 1200, height = 800)
barplot(
  profiles$infrastructure_viability_score,
  names.arg = profiles$system_name,
  horiz = TRUE,
  las = 1,
  main = "Infrastructure Viability Scores",
  xlab = "Viability score"
)
dev.off()

png(file.path(outputs_dir, "r_infrastructure_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$infrastructure_fragility_score,
  names.arg = profiles$system_name,
  horiz = TRUE,
  las = 1,
  main = "Infrastructure Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "system_name", "infrastructure_viability_score", "infrastructure_fragility_score")])
print(strategies[, c("strategy_id", "strategy_name", "infrastructure_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
