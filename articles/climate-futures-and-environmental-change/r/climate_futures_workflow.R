# Base R workflow for Climate Futures and Environmental Change.
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

profiles <- read.csv(file.path(data_dir, "climate_future_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "mitigation_adaptation_strategies.csv"))
risks <- read.csv(file.path(data_dir, "climate_risk_indicators.csv"))

profiles$climate_readiness_score <- round(
  -0.16 * profiles$emissions_intensity +
   0.15 * profiles$adaptation_capacity -
   0.15 * profiles$ecosystem_stress +
   0.14 * profiles$governance_coordination -
   0.12 * profiles$social_vulnerability +
   0.10 * profiles$technology_deployment +
   0.14 * profiles$transition_speed +
   0.12 * profiles$justice_capacity -
   0.10 * profiles$residual_loss,
  4
)

profiles$climate_fragility_score <- round(
  0.16 * profiles$emissions_intensity +
  0.15 * profiles$ecosystem_stress +
  0.14 * profiles$social_vulnerability +
  0.13 * profiles$residual_loss +
  0.12 * (1 - profiles$adaptation_capacity) +
  0.12 * (1 - profiles$governance_coordination) +
  0.10 * (1 - profiles$transition_speed) +
  0.08 * (1 - profiles$justice_capacity),
  4
)

profiles <- profiles[order(-profiles$climate_readiness_score), ]

strategies$climate_strategy_value_score <- round(
  0.17 * strategies$mitigation_effect +
  0.16 * strategies$adaptation_gain +
  0.15 * strategies$vulnerability_reduction +
  0.14 * strategies$ecosystem_protection +
  0.13 * strategies$governance_gain +
  0.11 * strategies$finance_capacity +
  0.10 * strategies$justice_gain +
  0.04 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$climate_strategy_value_score), ]

risks$climate_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$irreversibility +
  0.16 * risks$systemic_reach +
  0.12 * risks$visibility_gap +
  0.15 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$climate_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_climate_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_mitigation_adaptation_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_climate_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_climate_readiness_scores.png"), width = 1200, height = 800)
barplot(
  profiles$climate_readiness_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Climate Readiness Scores",
  xlab = "Readiness score"
)
dev.off()

png(file.path(outputs_dir, "r_climate_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$climate_fragility_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Climate Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "climate_readiness_score", "climate_fragility_score")])
print(strategies[, c("strategy_id", "strategy_name", "climate_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
