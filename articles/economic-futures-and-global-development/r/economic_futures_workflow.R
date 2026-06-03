# Base R workflow for Economic Futures and Global Development.
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

futures <- read.csv(file.path(data_dir, "development_futures.csv"))
policies <- read.csv(file.path(data_dir, "policy_portfolios.csv"))
shocks <- read.csv(file.path(data_dir, "shocks_and_stressors.csv"))

futures$development_quality_score <- round(
  0.14 * futures$growth -
  0.12 * futures$inequality -
  0.14 * futures$ecological_stress +
  0.13 * futures$institutional_capacity +
  0.12 * futures$resilience +
  0.08 * futures$fiscal_space +
  0.08 * futures$labor_inclusion +
  0.08 * futures$public_investment +
  0.06 * futures$technology_diffusion +
  0.03 * futures$trade_resilience +
  0.02 * futures$democratic_legitimacy,
  4
)

futures$development_fragility_score <- round(
  0.16 * futures$inequality +
  0.16 * futures$ecological_stress +
  0.13 * (1 - futures$institutional_capacity) +
  0.13 * (1 - futures$resilience) +
  0.12 * (1 - futures$fiscal_space) +
  0.10 * (1 - futures$labor_inclusion) +
  0.08 * (1 - futures$public_investment) +
  0.06 * (1 - futures$trade_resilience) +
  0.06 * (1 - futures$democratic_legitimacy),
  4
)

futures <- futures[order(-futures$development_quality_score), ]

policies$development_strategy_strength_score <- round(
  0.15 * policies$productive_capability +
  0.14 * policies$distributional_inclusion +
  0.14 * policies$ecological_viability +
  0.14 * policies$resilience_capacity +
  0.11 * policies$fiscal_sustainability +
  0.10 * policies$labor_protection +
  0.10 * policies$implementation_capacity +
  0.06 * policies$democratic_legitimacy +
  0.06 * (1 - policies$global_coordination_need),
  4
)

policies <- policies[order(-policies$development_strategy_strength_score), ]

shocks$development_shock_priority_score <- round(
  0.18 * shocks$probability_proxy +
  0.20 * shocks$severity +
  0.18 * shocks$systemic_reach +
  0.17 * shocks$distributional_exposure +
  0.15 * shocks$recovery_difficulty +
  0.12 * (1 - shocks$policy_preparedness),
  4
)

shocks <- shocks[order(-shocks$development_shock_priority_score), ]

write.csv(futures, file.path(outputs_dir, "r_development_future_scores.csv"), row.names = FALSE)
write.csv(policies, file.path(outputs_dir, "r_policy_portfolio_scores.csv"), row.names = FALSE)
write.csv(shocks, file.path(outputs_dir, "r_shock_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_development_quality_scores.png"), width = 1200, height = 800)
barplot(
  futures$development_quality_score,
  names.arg = futures$future_name,
  horiz = TRUE,
  las = 1,
  main = "Development Quality Scores",
  xlab = "Development quality"
)
dev.off()

png(file.path(outputs_dir, "r_development_fragility_scores.png"), width = 1200, height = 800)
barplot(
  futures$development_fragility_score,
  names.arg = futures$future_name,
  horiz = TRUE,
  las = 1,
  main = "Development Fragility Scores",
  xlab = "Development fragility"
)
dev.off()

print(futures[, c("future_id", "future_name", "development_quality_score", "development_fragility_score")])
print(policies[, c("policy_id", "policy_name", "development_strategy_strength_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
