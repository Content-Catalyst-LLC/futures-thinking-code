# Base R workflow for Global Governance Futures.
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
strategies <- read.csv(file.path(data_dir, "governance_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "governance_risk_indicators.csv"))

profiles$governance_capacity_score <- round(
  0.14 * profiles$institutional_capacity +
  0.16 * profiles$legitimacy +
  0.12 * profiles$legal_authority +
  0.11 * profiles$finance_capacity +
  0.13 * profiles$collective_action +
  0.10 * profiles$technology_governance +
  0.10 * profiles$planetary_risk_coordination +
  0.08 * profiles$adaptive_learning +
  0.08 * profiles$public_accountability +
  0.08 * profiles$representation_equity,
  4
)

profiles$legitimacy_gap_score <- round(
  0.18 * (1 - profiles$legitimacy) +
  0.14 * (1 - profiles$representation_equity) +
  0.13 * (1 - profiles$public_accountability) +
  0.12 * (1 - profiles$legal_authority) +
  0.11 * (1 - profiles$collective_action) +
  0.10 * (1 - profiles$finance_capacity) +
  0.08 * (1 - profiles$institutional_capacity) +
  0.07 * (1 - profiles$technology_governance) +
  0.04 * (1 - profiles$planetary_risk_coordination) +
  0.03 * (1 - profiles$adaptive_learning),
  4
)

profiles <- profiles[order(-profiles$governance_capacity_score), ]

strategies$governance_strategy_value_score <- round(
  0.13 * strategies$representation_gain +
  0.12 * strategies$finance_gain +
  0.12 * strategies$legal_accountability_gain +
  0.11 * strategies$climate_governance_gain +
  0.09 * strategies$health_governance_gain +
  0.10 * strategies$technology_governance_gain +
  0.08 * strategies$migration_protection_gain +
  0.08 * strategies$security_coordination_gain +
  0.08 * strategies$civil_society_gain +
  0.04 * strategies$implementation_capacity +
  0.05 * strategies$public_legitimacy_gain,
  4
)

strategies <- strategies[order(-strategies$governance_strategy_value_score), ]

risks$governance_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$cascade_potential +
  0.12 * risks$visibility_gap +
  0.14 * risks$recovery_difficulty +
  0.17 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$governance_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_governance_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_governance_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_governance_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_governance_capacity_scores.png"), width = 1200, height = 800)
barplot(
  profiles$governance_capacity_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Global Governance Capacity Scores",
  xlab = "Governance capacity score"
)
dev.off()

png(file.path(outputs_dir, "r_legitimacy_gap_scores.png"), width = 1200, height = 800)
barplot(
  profiles$legitimacy_gap_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Global Governance Legitimacy Gap Scores",
  xlab = "Legitimacy gap score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "governance_capacity_score", "legitimacy_gap_score")])
print(strategies[, c("strategy_id", "strategy_name", "governance_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
