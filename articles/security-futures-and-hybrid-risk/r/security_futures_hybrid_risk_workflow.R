# Base R workflow for Security Futures and Hybrid Risk.
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

profiles <- read.csv(file.path(data_dir, "security_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "security_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "security_risk_indicators.csv"))
dependencies <- read.csv(file.path(data_dir, "infrastructure_dependencies.csv"))

profiles$hybrid_risk_score <- round(
  0.13 * profiles$cyber_exposure +
  0.13 * profiles$infrastructure_dependence +
  0.13 * profiles$information_vulnerability +
  0.12 * profiles$climate_security_stress +
  0.10 * profiles$resource_dependence +
  0.11 * (1 - profiles$institutional_coordination) +
  0.10 * (1 - profiles$civilian_protection) +
  0.10 * (1 - profiles$adaptive_resilience) +
  0.05 * (1 - profiles$public_trust) +
  0.03 * (1 - profiles$attribution_clarity),
  4
)

profiles$security_resilience_score <- round(
  0.20 * profiles$institutional_coordination +
  0.22 * profiles$civilian_protection +
  0.22 * profiles$adaptive_resilience +
  0.16 * profiles$public_trust +
  0.08 * profiles$attribution_clarity +
  0.04 * (1 - profiles$cyber_exposure) +
  0.04 * (1 - profiles$information_vulnerability) +
  0.04 * (1 - profiles$infrastructure_dependence),
  4
)

profiles$resilience_gap_score <- pmax(0, profiles$hybrid_risk_score - profiles$security_resilience_score)
profiles <- profiles[order(-profiles$hybrid_risk_score), ]

strategies$security_strategy_value_score <- round(
  0.12 * strategies$cyber_resilience_gain +
  0.12 * strategies$infrastructure_redundancy_gain +
  0.12 * strategies$information_integrity_gain +
  0.10 * strategies$climate_security_adaptation_gain +
  0.09 * strategies$resource_security_gain +
  0.12 * strategies$institutional_coordination_gain +
  0.12 * strategies$civilian_protection_gain +
  0.07 * strategies$deterrence_gain +
  0.08 * strategies$adaptive_learning_gain +
  0.03 * strategies$implementation_capacity +
  0.03 * strategies$public_legitimacy_gain,
  4
)

strategies <- strategies[order(-strategies$security_strategy_value_score), ]

risks$hybrid_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.18 * risks$cascade_potential +
  0.10 * risks$visibility_gap +
  0.13 * risks$recovery_difficulty +
  0.17 * risks$distributional_harm +
  0.10 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$hybrid_risk_priority_score), ]

dependencies$cascade_exposure_score <- round(
  dependencies$dependency_weight *
  dependencies$disruption_sensitivity *
  dependencies$public_harm_potential *
  (1 - dependencies$recovery_capacity),
  4
)

dependencies <- dependencies[order(-dependencies$cascade_exposure_score), ]

write.csv(profiles, file.path(outputs_dir, "r_security_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_security_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_hybrid_risk_priority_scores.csv"), row.names = FALSE)
write.csv(dependencies, file.path(outputs_dir, "r_infrastructure_cascade_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_hybrid_risk_scores.png"), width = 1200, height = 800)
barplot(
  profiles$hybrid_risk_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Hybrid Risk Scores",
  xlab = "Hybrid risk score"
)
dev.off()

png(file.path(outputs_dir, "r_security_resilience_scores.png"), width = 1200, height = 800)
barplot(
  profiles$security_resilience_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Security Resilience Scores",
  xlab = "Security resilience score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "hybrid_risk_score", "security_resilience_score", "resilience_gap_score")])
print(strategies[, c("strategy_id", "strategy_name", "security_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
