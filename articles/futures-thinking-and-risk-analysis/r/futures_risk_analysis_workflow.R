# Base R workflow for Futures Thinking and Risk Analysis.
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

profiles <- read.csv(file.path(data_dir, "risk_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "strategy_options.csv"))
indicators <- read.csv(file.path(data_dir, "risk_indicators.csv"))

profiles$futures_risk_profile_score <- round(
  0.12 * (1 - profiles$probability_confidence) +
  0.16 * profiles$structural_uncertainty +
  0.14 * profiles$interdependence +
  0.15 * profiles$vulnerability -
  0.11 * profiles$resilience_capacity -
  0.10 * profiles$governance_capacity -
  0.08 * profiles$signal_visibility +
  0.12 * profiles$tail_risk_severity +
  0.10 * profiles$distributional_harm -
  0.02 * profiles$adaptive_capacity,
  4
)

profiles$preparedness_gap_score <- round(
  0.18 * (1 - profiles$resilience_capacity) +
  0.18 * (1 - profiles$governance_capacity) +
  0.15 * (1 - profiles$signal_visibility) +
  0.15 * profiles$structural_uncertainty +
  0.12 * profiles$vulnerability +
  0.10 * profiles$tail_risk_severity +
  0.08 * profiles$distributional_harm +
  0.04 * (1 - profiles$adaptive_capacity),
  4
)

profiles <- profiles[order(-profiles$futures_risk_profile_score), ]

performance_cols <- c(
  "baseline_performance",
  "technology_disruption_performance",
  "climate_stress_performance",
  "geopolitical_fragmentation_performance",
  "financial_contagion_performance",
  "institutional_breakdown_performance",
  "systemic_cascade_performance"
)

strategy_scores <- data.frame(
  strategy_id = strategies$strategy_id,
  strategy_name = strategies$strategy_name,
  strategy_type = strategies$strategy_type,
  mean_performance = apply(strategies[, performance_cols], 1, mean),
  worst_case = apply(strategies[, performance_cols], 1, min),
  best_case = apply(strategies[, performance_cols], 1, max)
)

scenario_best <- apply(strategies[, performance_cols], 2, max)
max_regrets <- c()
mean_regrets <- c()

for (i in seq_len(nrow(strategies))) {
  regrets <- scenario_best - as.numeric(strategies[i, performance_cols])
  max_regrets <- c(max_regrets, max(regrets))
  mean_regrets <- c(mean_regrets, mean(regrets))
}

strategy_scores$maximum_regret <- max_regrets
strategy_scores$mean_regret <- mean_regrets
strategy_scores$governance_quality <- (
  0.30 * strategies$monitoring_capacity +
  0.30 * strategies$adaptability +
  0.20 * strategies$implementation_capacity +
  0.20 * strategies$public_legitimacy
)
strategy_scores$robustness_score <- round(
  0.42 * strategy_scores$worst_case +
  0.28 * strategy_scores$mean_performance -
  0.20 * strategy_scores$maximum_regret +
  0.10 * strategy_scores$governance_quality,
  4
)

strategy_scores <- strategy_scores[order(-strategy_scores$robustness_score), ]

indicators$risk_indicator_priority_score <- round(
  0.13 * indicators$signal_strength +
  0.11 * indicators$visibility_gap +
  0.09 * (1 - indicators$lead_time) +
  0.15 * indicators$systemic_relevance +
  0.16 * indicators$cascade_potential +
  0.15 * indicators$tail_severity +
  0.11 * indicators$preparedness_gap +
  0.10 * indicators$distributional_harm,
  4
)

indicators <- indicators[order(-indicators$risk_indicator_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_risk_profile_scores.csv"), row.names = FALSE)
write.csv(strategy_scores, file.path(outputs_dir, "r_strategy_robustness_scores.csv"), row.names = FALSE)
write.csv(indicators, file.path(outputs_dir, "r_risk_indicator_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_futures_risk_profile_scores.png"), width = 1200, height = 800)
barplot(
  profiles$futures_risk_profile_score,
  names.arg = profiles$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Futures Risk Profile Scores",
  xlab = "Risk profile score"
)
dev.off()

png(file.path(outputs_dir, "r_strategy_robustness_scores.png"), width = 1200, height = 800)
barplot(
  strategy_scores$robustness_score,
  names.arg = strategy_scores$strategy_name,
  horiz = TRUE,
  las = 1,
  main = "Strategy Robustness Scores",
  xlab = "Robustness score"
)
dev.off()

print(profiles[, c("profile_id", "scenario_name", "futures_risk_profile_score", "preparedness_gap_score")])
print(strategy_scores[, c("strategy_id", "strategy_name", "robustness_score", "worst_case", "maximum_regret")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
