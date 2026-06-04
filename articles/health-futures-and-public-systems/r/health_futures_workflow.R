# Base R workflow for Health Futures and Public Systems.
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

profiles <- read.csv(file.path(data_dir, "health_system_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "health_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "health_risk_indicators.csv"))

profiles$public_health_resilience_score <- round(
  0.13 * profiles$prevention_capacity +
  0.12 * profiles$healthcare_access +
  0.15 * profiles$public_health_infrastructure +
  0.10 * profiles$climate_readiness +
  0.11 * profiles$workforce_resilience +
  0.08 * profiles$technology_governance +
  0.11 * profiles$social_protection +
  0.08 * profiles$public_trust +
  0.07 * profiles$equity_capacity +
  0.05 * profiles$care_capacity,
  4
)

profiles$health_system_fragility_score <- round(
  0.13 * (1 - profiles$prevention_capacity) +
  0.12 * (1 - profiles$healthcare_access) +
  0.15 * (1 - profiles$public_health_infrastructure) +
  0.11 * (1 - profiles$climate_readiness) +
  0.13 * (1 - profiles$workforce_resilience) +
  0.08 * (1 - profiles$technology_governance) +
  0.10 * (1 - profiles$social_protection) +
  0.08 * (1 - profiles$public_trust) +
  0.06 * (1 - profiles$equity_capacity) +
  0.04 * (1 - profiles$care_capacity),
  4
)

profiles <- profiles[order(-profiles$public_health_resilience_score), ]

strategies$health_strategy_value_score <- round(
  0.13 * strategies$prevention_gain +
  0.12 * strategies$access_gain +
  0.14 * strategies$public_health_gain +
  0.11 * strategies$climate_health_gain +
  0.11 * strategies$workforce_gain +
  0.08 * strategies$technology_governance_gain +
  0.10 * strategies$social_protection_gain +
  0.08 * strategies$trust_gain +
  0.08 * strategies$equity_gain +
  0.04 * strategies$care_gain +
  0.01 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$health_strategy_value_score), ]

risks$health_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$cascade_potential +
  0.12 * risks$visibility_gap +
  0.14 * risks$recovery_difficulty +
  0.17 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$health_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_health_system_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_health_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_health_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_health_resilience_scores.png"), width = 1200, height = 800)
barplot(
  profiles$public_health_resilience_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Public Health Resilience Scores",
  xlab = "Resilience score"
)
dev.off()

png(file.path(outputs_dir, "r_health_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$health_system_fragility_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Health System Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "public_health_resilience_score", "health_system_fragility_score")])
print(strategies[, c("strategy_id", "strategy_name", "health_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
