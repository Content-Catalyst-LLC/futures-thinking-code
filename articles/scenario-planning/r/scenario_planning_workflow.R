# Base R workflow for Scenario Planning.
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

strategies <- read.csv(file.path(data_dir, "strategies.csv"))
performance <- read.csv(file.path(data_dir, "strategy_performance.csv"))
drivers <- read.csv(file.path(data_dir, "drivers_uncertainties.csv"))
signals <- read.csv(file.path(data_dir, "signals.csv"))

merged <- merge(performance, strategies, by = "strategy_id")

mean_perf <- aggregate(performance ~ strategy_id + strategy + strategy_type, data = merged, FUN = mean)
names(mean_perf)[names(mean_perf) == "performance"] <- "mean_performance"

worst_perf <- aggregate(performance ~ strategy_id, data = merged, FUN = min)
names(worst_perf)[2] <- "worst_case"

best_perf <- aggregate(performance ~ strategy_id, data = merged, FUN = max)
names(best_perf)[2] <- "best_case"

summary <- merge(mean_perf, worst_perf, by = "strategy_id")
summary <- merge(summary, best_perf, by = "strategy_id")
summary$robustness_proxy <- round(
  0.55 * summary$worst_case + 0.45 * summary$mean_performance,
  4
)
summary <- summary[order(-summary$robustness_proxy), ]

drivers$criticality_score <- round(drivers$uncertainty * drivers$impact * drivers$velocity, 4)
drivers <- drivers[order(-drivers$criticality_score), ]

signals$watch_score <- round(
  0.35 * signals$uncertainty + 0.40 * signals$impact + 0.25 * signals$novelty,
  4
)
signals <- signals[order(-signals$watch_score), ]

write.csv(summary, file.path(outputs_dir, "r_strategy_robustness_proxy.csv"), row.names = FALSE)
write.csv(drivers, file.path(outputs_dir, "r_driver_uncertainty_scores.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_signal_watch_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_strategy_robustness_proxy.png"), width = 1100, height = 700)
barplot(
  summary$robustness_proxy,
  names.arg = summary$strategy,
  horiz = TRUE,
  las = 1,
  main = "Scenario Strategy Robustness Proxy",
  xlab = "Robustness proxy"
)
dev.off()

print(summary[, c("strategy", "mean_performance", "worst_case", "best_case", "robustness_proxy")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
