# Base R workflow for Trend Analysis and Megatrends.
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

trends <- read.csv(file.path(data_dir, "trend_profiles.csv"))
signals <- read.csv(file.path(data_dir, "signals.csv"))
indicators <- read.csv(file.path(data_dir, "indicators.csv"))

trends$long_term_change_profile <- round(
  0.20 * trends$momentum +
  0.22 * trends$structural_depth +
  0.22 * trends$cross_system_influence -
  0.12 * trends$reversibility -
  0.14 * trends$uncertainty +
  0.10 * trends$distributional_sensitivity,
  4
)

trends$classification <- ifelse(
  trends$long_term_change_profile >= 0.55,
  "Megatrend-level structural force",
  ifelse(
    trends$long_term_change_profile >= 0.48,
    "Megatrend candidate",
    ifelse(
      trends$long_term_change_profile >= 0.42,
      "Established strategic trend",
      "Emerging or domain-specific trend"
    )
  )
)

trends <- trends[order(-trends$long_term_change_profile), ]

signals$watch_score <- round(
  0.35 * signals$uncertainty +
  0.40 * signals$impact +
  0.25 * signals$novelty,
  4
)
signals <- signals[order(-signals$watch_score), ]

indicators$movement_score <- round(
  (indicators$current_value - indicators$baseline_value) * indicators$confidence,
  4
)
indicators <- indicators[order(-indicators$movement_score), ]

write.csv(trends, file.path(outputs_dir, "r_trend_megatrend_profiles.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_signal_watch_scores.csv"), row.names = FALSE)
write.csv(indicators, file.path(outputs_dir, "r_indicator_movement_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_trend_megatrend_profiles.png"), width = 1100, height = 700)
barplot(
  trends$long_term_change_profile,
  names.arg = trends$pattern_type,
  horiz = TRUE,
  las = 1,
  main = "Trend and Megatrend Profiles",
  xlab = "Long-term change profile"
)
dev.off()

print(trends[, c("pattern_type", "domain", "long_term_change_profile", "classification")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
