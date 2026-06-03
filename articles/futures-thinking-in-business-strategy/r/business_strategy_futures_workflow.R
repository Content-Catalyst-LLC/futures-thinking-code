# Base R workflow for Futures Thinking in Business Strategy.
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

strategies <- read.csv(file.path(data_dir, "strategy_profiles.csv"))
options <- read.csv(file.path(data_dir, "strategic_options.csv"))
capabilities <- read.csv(file.path(data_dir, "capability_register.csv"))

strategies$business_futures_readiness_score <- round(
  0.14 * strategies$innovation_capacity -
  0.10 * strategies$uncertainty_exposure +
  0.15 * strategies$resilience +
  0.14 * strategies$strategic_flexibility +
  0.10 * strategies$organizational_alignment +
  0.12 * strategies$sensing_capability +
  0.08 * strategies$capital_flexibility +
  0.09 * strategies$legitimacy_trust +
  0.08 * strategies$transition_readiness,
  4
)

strategies$strategic_fragility_score <- round(
  0.18 * strategies$uncertainty_exposure +
  0.14 * (1 - strategies$resilience) +
  0.14 * (1 - strategies$strategic_flexibility) +
  0.13 * (1 - strategies$sensing_capability) +
  0.11 * (1 - strategies$capital_flexibility) +
  0.10 * (1 - strategies$organizational_alignment) +
  0.10 * (1 - strategies$legitimacy_trust) +
  0.10 * (1 - strategies$transition_readiness),
  4
)

strategies <- strategies[order(-strategies$business_futures_readiness_score), ]

options$net_strategic_option_value <- round(
  0.22 * options$learning_value +
  0.20 * options$upside_potential +
  0.15 * options$reversibility +
  0.15 * options$scalability +
  0.14 * options$strategic_fit +
  0.14 * options$signal_sensitivity -
  0.20 * options$cost_to_maintain,
  4
)

options <- options[order(-options$net_strategic_option_value), ]

capabilities$future_capability_gap <- pmax(0, capabilities$future_importance - capabilities$current_strength)
capabilities$capability_investment_priority <- round(
  0.34 * capabilities$future_importance +
  0.20 * capabilities$development_difficulty +
  0.18 * capabilities$coordination_requirement +
  0.14 * capabilities$investment_need +
  0.14 * (1 - capabilities$current_strength),
  4
)

capabilities <- capabilities[order(-capabilities$capability_investment_priority), ]

write.csv(strategies, file.path(outputs_dir, "r_strategy_profile_scores.csv"), row.names = FALSE)
write.csv(options, file.path(outputs_dir, "r_strategic_option_scores.csv"), row.names = FALSE)
write.csv(capabilities, file.path(outputs_dir, "r_capability_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_business_futures_readiness_scores.png"), width = 1200, height = 800)
barplot(
  strategies$business_futures_readiness_score,
  names.arg = strategies$strategy_name,
  horiz = TRUE,
  las = 1,
  main = "Business Futures Readiness Scores",
  xlab = "Readiness score"
)
dev.off()

png(file.path(outputs_dir, "r_strategic_fragility_scores.png"), width = 1200, height = 800)
barplot(
  strategies$strategic_fragility_score,
  names.arg = strategies$strategy_name,
  horiz = TRUE,
  las = 1,
  main = "Strategic Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(strategies[, c("strategy_id", "strategy_name", "business_futures_readiness_score", "strategic_fragility_score")])
print(options[, c("option_id", "option_name", "net_strategic_option_value")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
