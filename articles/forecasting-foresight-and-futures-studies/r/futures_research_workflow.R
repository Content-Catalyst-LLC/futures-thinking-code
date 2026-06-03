# Base R workflow for Futures Thinking article directories.
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

profiles <- read.csv(file.path(data_dir, "practice_profiles.csv"))
signals <- read.csv(file.path(data_dir, "signals.csv"))
drivers <- read.csv(file.path(data_dir, "drivers.csv"))
assumptions <- read.csv(file.path(data_dir, "assumptions.csv"))
performance <- read.csv(file.path(data_dir, "strategy_performance.csv"))
strategies <- read.csv(file.path(data_dir, "strategies.csv"))

weights <- c(
  predictive_emphasis = 0.04,
  uncertainty_plurality = 0.20,
  assumption_visibility = 0.18,
  participatory_depth = 0.14,
  strategic_readiness = 0.20,
  critical_reflection = 0.14,
  reproducibility = 0.10
)

practice_scores <- data.frame(
  practice = profiles$practice,
  anticipatory_capacity_score = numeric(nrow(profiles)),
  strongest_dimension = character(nrow(profiles)),
  weakest_dimension = character(nrow(profiles)),
  stringsAsFactors = FALSE
)

for (i in seq_len(nrow(profiles))) {
  vals <- as.numeric(profiles[i, names(weights)])
  names(vals) <- names(weights)
  practice_scores$anticipatory_capacity_score[i] <- round(sum(vals * weights), 4)
  practice_scores$strongest_dimension[i] <- names(vals)[which.max(vals)]
  practice_scores$weakest_dimension[i] <- names(vals)[which.min(vals)]
}

practice_scores <- practice_scores[order(-practice_scores$anticipatory_capacity_score), ]

signals$watch_score <- round(
  0.35 * signals$uncertainty + 0.40 * signals$impact + 0.25 * signals$novelty,
  4
)

drivers$driver_priority <- round(
  drivers$uncertainty * drivers$impact * drivers$velocity,
  4
)

assumptions$vulnerability_score <- round(
  assumptions$exposure * (1 - assumptions$confidence) * (1 + (1 - assumptions$reversibility)),
  4
)

merged <- merge(performance, strategies, by = "strategy_id")
strategy_summary <- aggregate(
  performance ~ strategy_id + strategy_name + strategy_type,
  data = merged,
  FUN = mean
)
names(strategy_summary)[names(strategy_summary) == "performance"] <- "mean_performance"

worst <- aggregate(performance ~ strategy_id, data = merged, FUN = min)
names(worst)[2] <- "worst_case"

best <- aggregate(performance ~ strategy_id, data = merged, FUN = max)
names(best)[2] <- "best_case"

strategy_summary <- merge(strategy_summary, worst, by = "strategy_id")
strategy_summary <- merge(strategy_summary, best, by = "strategy_id")
strategy_summary$robustness_proxy <- round(
  0.55 * strategy_summary$worst_case + 0.45 * strategy_summary$mean_performance,
  4
)
strategy_summary <- strategy_summary[order(-strategy_summary$robustness_proxy), ]

write.csv(practice_scores, file.path(outputs_dir, "r_practice_profile_scores.csv"), row.names = FALSE)
write.csv(signals[order(-signals$watch_score), ], file.path(outputs_dir, "r_signal_watch_scores.csv"), row.names = FALSE)
write.csv(drivers[order(-drivers$driver_priority), ], file.path(outputs_dir, "r_driver_priority_scores.csv"), row.names = FALSE)
write.csv(assumptions[order(-assumptions$vulnerability_score), ], file.path(outputs_dir, "r_assumption_vulnerability_scores.csv"), row.names = FALSE)
write.csv(strategy_summary, file.path(outputs_dir, "r_strategy_robustness_proxy.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_strategy_robustness_proxy.png"), width = 1100, height = 700)
barplot(
  strategy_summary$robustness_proxy,
  names.arg = strategy_summary$strategy_name,
  horiz = TRUE,
  las = 1,
  main = "Strategy Robustness Proxy",
  xlab = "Robustness proxy"
)
dev.off()

print(practice_scores)
print(strategy_summary)
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
