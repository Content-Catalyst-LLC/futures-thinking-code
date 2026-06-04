# Base R workflow for Urban Futures.
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

profiles <- read.csv(file.path(data_dir, "urban_system_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "urban_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "urban_risk_indicators.csv"))

profiles$urban_viability_score <- round(
  0.17 * profiles$infrastructure_strength +
  0.16 * profiles$governance_capacity +
  0.14 * profiles$housing_affordability -
  0.14 * profiles$climate_exposure -
  0.14 * profiles$inequality +
  0.09 * profiles$digital_integration +
  0.12 * profiles$public_finance_capacity +
  0.14 * profiles$social_cohesion -
  0.08 * profiles$maintenance_backlog,
  4
)

profiles$urban_fragility_score <- round(
  0.15 * profiles$climate_exposure +
  0.15 * profiles$inequality +
  0.14 * profiles$maintenance_backlog +
  0.13 * (1 - profiles$infrastructure_strength) +
  0.13 * (1 - profiles$governance_capacity) +
  0.12 * (1 - profiles$housing_affordability) +
  0.10 * (1 - profiles$public_finance_capacity) +
  0.10 * (1 - profiles$social_cohesion) +
  0.08 * profiles$digital_integration,
  4
)

profiles <- profiles[order(-profiles$urban_viability_score), ]

strategies$urban_strategy_value_score <- round(
  0.16 * strategies$infrastructure_gain +
  0.16 * strategies$housing_stability_gain +
  0.14 * strategies$climate_resilience_gain +
  0.14 * strategies$governance_gain +
  0.12 * strategies$finance_gain +
  0.10 * strategies$digital_accountability_gain +
  0.14 * strategies$social_cohesion_gain +
  0.04 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$urban_strategy_value_score), ]

risks$urban_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$cascade_potential +
  0.12 * risks$visibility_gap +
  0.14 * risks$recovery_difficulty +
  0.17 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$urban_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_urban_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_urban_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_urban_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_urban_viability_scores.png"), width = 1200, height = 800)
barplot(
  profiles$urban_viability_score,
  names.arg = profiles$city_future_name,
  horiz = TRUE,
  las = 1,
  main = "Urban Viability Scores",
  xlab = "Viability score"
)
dev.off()

png(file.path(outputs_dir, "r_urban_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$urban_fragility_score,
  names.arg = profiles$city_future_name,
  horiz = TRUE,
  las = 1,
  main = "Urban Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "city_future_name", "urban_viability_score", "urban_fragility_score")])
print(strategies[, c("strategy_id", "strategy_name", "urban_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
