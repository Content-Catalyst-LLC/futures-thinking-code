# Base R workflow for Possible, Plausible, Probable, and Preferable Futures.
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

futures <- read.csv(file.path(data_dir, "candidate_futures.csv"))
strategies <- read.csv(file.path(data_dir, "strategies.csv"))

futures$plausibility_score <- round(
  0.40 * futures$driver_support +
  0.35 * futures$pathway_coherence +
  0.25 * futures$constraint_fit,
  4
)

futures$probability_score <- round(
  0.70 * futures$current_trend_strength +
  0.30 * futures$driver_support,
  4
)

futures$preference_score <- round(
  0.30 * futures$justice_value +
  0.25 * futures$sustainability_value +
  0.25 * futures$resilience_value +
  0.20 * futures$legitimacy_value,
  4
)

futures$strategic_priority <- round(
  0.35 * futures$plausibility_score +
  0.25 * futures$probability_score +
  0.40 * futures$preference_score,
  4
)

futures <- futures[order(-futures$strategic_priority), ]

strategies$category_fit_score <- round(
  0.20 * strategies$probable_fit +
  0.30 * strategies$plausible_fit +
  0.30 * strategies$preferable_fit +
  0.20 * strategies$adaptive_capacity -
  0.05 * strategies$implementation_difficulty +
  0.05 * strategies$equity_sensitivity,
  4
)

strategies <- strategies[order(-strategies$category_fit_score), ]

write.csv(futures, file.path(outputs_dir, "r_future_category_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_strategy_category_fit.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_future_strategic_priority.png"), width = 1100, height = 700)
barplot(
  futures$strategic_priority,
  names.arg = futures$future,
  horiz = TRUE,
  las = 1,
  main = "Strategic Priority Across Candidate Futures",
  xlab = "Strategic priority"
)
dev.off()

print(futures[, c("future", "plausibility_score", "probability_score", "preference_score", "strategic_priority")])
print(strategies[, c("strategy", "category_fit_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
