# Base R workflow for Weak Signals and Early Indicators.
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

signals <- read.csv(file.path(data_dir, "weak_signals.csv"))
indicators <- read.csv(file.path(data_dir, "early_indicators.csv"))
clusters <- read.csv(file.path(data_dir, "signal_clusters.csv"))

signals$weak_signal_profile <- round(
  0.10 * signals$visibility -
  0.08 * signals$ambiguity +
  0.24 * signals$systemic_connection +
  0.22 * signals$propagation_potential +
  0.12 * signals$institutional_recognition +
  0.12 * signals$distributional_relevance +
  0.20 * signals$monitoring_urgency,
  4
)

signals$priority_class <- ifelse(
  signals$weak_signal_profile >= 0.72,
  "High-priority watchlist",
  ifelse(
    signals$weak_signal_profile >= 0.62,
    "Monitor and cluster",
    ifelse(
      signals$weak_signal_profile >= 0.54,
      "Exploratory monitoring",
      "Low-priority or background noise"
    )
  )
)

signals <- signals[order(-signals$weak_signal_profile), ]

indicators$evidence_index <- indicators$evidence_count / max(indicators$evidence_count)
indicators$early_indicator_score <- round(
  0.25 * indicators$repetition_score +
  0.25 * indicators$clarity_score +
  0.20 * indicators$measurement_quality +
  0.20 * indicators$policy_attention +
  0.10 * indicators$evidence_index,
  4
)

indicators <- indicators[order(-indicators$early_indicator_score), ]

clusters$cluster_priority <- round(clusters$coherence * clusters$strategic_concern, 4)
clusters <- clusters[order(-clusters$cluster_priority), ]

write.csv(signals, file.path(outputs_dir, "r_weak_signal_profiles.csv"), row.names = FALSE)
write.csv(indicators, file.path(outputs_dir, "r_early_indicator_scores.csv"), row.names = FALSE)
write.csv(clusters, file.path(outputs_dir, "r_signal_cluster_priorities.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_weak_signal_profiles.png"), width = 1200, height = 800)
barplot(
  signals$weak_signal_profile,
  names.arg = signals$signal_title,
  horiz = TRUE,
  las = 1,
  main = "Weak Signal Profiles",
  xlab = "Profile score"
)
dev.off()

print(signals[, c("signal_title", "domain", "signal_type", "weak_signal_profile", "priority_class")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
