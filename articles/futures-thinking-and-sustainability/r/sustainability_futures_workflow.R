# Base R workflow for Futures Thinking and Sustainability.
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

profiles <- read.csv(file.path(data_dir, "sustainability_future_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "transition_strategies.csv"))
risks <- read.csv(file.path(data_dir, "sustainability_risk_indicators.csv"))

profiles$sustainability_viability_score <- round(
  0.17 * profiles$ecological_integrity +
  0.15 * profiles$social_equity +
  0.14 * profiles$adaptive_capacity +
  0.10 * profiles$technological_responsibility +
  0.14 * profiles$governance_coordination +
  0.10 * profiles$public_finance_capacity +
  0.10 * profiles$resilience_capacity +
  0.10 * profiles$justice_legitimacy -
  0.08 * profiles$degradation_pressure,
  4
)

profiles$sustainability_fragility_score <- round(
  0.16 * profiles$degradation_pressure +
  0.15 * (1 - profiles$ecological_integrity) +
  0.14 * (1 - profiles$social_equity) +
  0.13 * (1 - profiles$governance_coordination) +
  0.12 * (1 - profiles$adaptive_capacity) +
  0.11 * (1 - profiles$public_finance_capacity) +
  0.10 * (1 - profiles$resilience_capacity) +
  0.09 * (1 - profiles$justice_legitimacy),
  4
)

profiles <- profiles[order(-profiles$sustainability_viability_score), ]

strategies$sustainability_gain_score <- round(
  0.16 * strategies$ecological_gain +
  0.16 * strategies$equity_gain +
  0.14 * strategies$adaptive_capacity_gain +
  0.14 * strategies$governance_gain +
  0.12 * strategies$finance_gain +
  0.12 * strategies$resilience_gain +
  0.12 * strategies$justice_gain +
  0.04 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$sustainability_gain_score), ]

risks$sustainability_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$irreversibility +
  0.16 * risks$systemic_reach +
  0.12 * risks$visibility_gap +
  0.15 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$sustainability_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_sustainability_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_transition_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_sustainability_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_sustainability_viability_scores.png"), width = 1200, height = 800)
barplot(
  profiles$sustainability_viability_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Sustainability Viability Scores",
  xlab = "Viability score"
)
dev.off()

png(file.path(outputs_dir, "r_sustainability_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$sustainability_fragility_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Sustainability Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "sustainability_viability_score", "sustainability_fragility_score")])
print(strategies[, c("strategy_id", "strategy_name", "sustainability_gain_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
