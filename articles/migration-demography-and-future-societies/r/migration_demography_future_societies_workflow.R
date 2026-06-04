# Base R workflow for Migration, Demography, and Future Societies.
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

profiles <- read.csv(file.path(data_dir, "demographic_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "demographic_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "demographic_risk_indicators.csv"))
care_records <- read.csv(file.path(data_dir, "care_urban_records.csv"))

profiles$demographic_stress_score <- round(
  0.13 * profiles$aging_pressure +
  0.13 * profiles$youth_opportunity_gap +
  0.12 * profiles$migration_pressure +
  0.13 * (1 - profiles$care_capacity) +
  0.12 * profiles$housing_pressure +
  0.10 * (1 - profiles$labor_adaptation) +
  0.11 * profiles$climate_mobility_exposure +
  0.08 * (1 - profiles$social_cohesion) +
  0.05 * (1 - profiles$gender_equity) +
  0.03 * (1 - profiles$public_health_capacity),
  4
)

profiles$adaptive_capacity_score <- round(
  0.18 * profiles$care_capacity +
  0.16 * profiles$labor_adaptation +
  0.16 * profiles$social_cohesion +
  0.13 * profiles$gender_equity +
  0.13 * profiles$public_health_capacity +
  0.10 * (1 - profiles$housing_pressure) +
  0.08 * (1 - profiles$youth_opportunity_gap) +
  0.06 * (1 - profiles$climate_mobility_exposure),
  4
)

profiles$adaptation_gap_score <- pmax(0, profiles$demographic_stress_score - profiles$adaptive_capacity_score)
profiles <- profiles[order(-profiles$demographic_stress_score), ]

strategies$demographic_strategy_value_score <- round(
  0.13 * strategies$care_investment_gain +
  0.12 * strategies$housing_affordability_gain +
  0.12 * strategies$youth_opportunity_gain +
  0.12 * strategies$legal_mobility_gain +
  0.11 * strategies$labor_protection_gain +
  0.10 * strategies$climate_adaptation_gain +
  0.09 * strategies$reproductive_health_gain +
  0.08 * strategies$gender_equity_gain +
  0.07 * strategies$public_health_gain +
  0.04 * strategies$social_cohesion_gain +
  0.02 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$demographic_strategy_value_score), ]

risks$demographic_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.15 * risks$cascade_potential +
  0.10 * risks$visibility_gap +
  0.13 * risks$recovery_difficulty +
  0.20 * risks$distributional_harm +
  0.10 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$demographic_risk_priority_score), ]

care_records$care_stress_score <- round(
  0.28 * care_records$eldercare_demand +
  0.20 * care_records$childcare_demand +
  0.20 * care_records$unpaid_care_burden +
  0.14 * (1 - care_records$care_workforce_capacity) +
  0.10 * (1 - care_records$public_health_capacity) +
  0.08 * (1 - care_records$integration_capacity),
  4
)

care_records <- care_records[order(-care_records$care_stress_score), ]

write.csv(profiles, file.path(outputs_dir, "r_demographic_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_demographic_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_demographic_risk_priority_scores.csv"), row.names = FALSE)
write.csv(care_records, file.path(outputs_dir, "r_care_urban_capacity_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_demographic_stress_scores.png"), width = 1200, height = 800)
barplot(
  profiles$demographic_stress_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Demographic Stress Scores",
  xlab = "Demographic stress score"
)
dev.off()

png(file.path(outputs_dir, "r_adaptive_capacity_scores.png"), width = 1200, height = 800)
barplot(
  profiles$adaptive_capacity_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Demographic Adaptive Capacity Scores",
  xlab = "Adaptive capacity score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "demographic_stress_score", "adaptive_capacity_score", "adaptation_gap_score")])
print(strategies[, c("strategy_id", "strategy_name", "demographic_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
