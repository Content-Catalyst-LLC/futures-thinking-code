# Base R workflow for Horizon Scanning.
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

signals <- read.csv(file.path(data_dir, "signals.csv"))
clusters <- read.csv(file.path(data_dir, "signal_clusters.csv"))
institutions <- read.csv(file.path(data_dir, "institutional_profiles.csv"))

signals$horizon_scanning_profile <- round(
  0.10 * signals$visibility -
  0.08 * signals$ambiguity +
  0.22 * signals$structural_connection +
  0.18 * signals$domain_diversity +
  0.14 * signals$source_diversity +
  0.14 * signals$assumption_challenge +
  0.30 * signals$strategic_relevance,
  4
)

signals$priority_class <- ifelse(
  signals$horizon_scanning_profile >= 0.72,
  "High-priority watchlist",
  ifelse(
    signals$horizon_scanning_profile >= 0.62,
    "Monitor and cluster",
    ifelse(
      signals$horizon_scanning_profile >= 0.54,
      "Exploratory monitoring",
      "Low-priority or background noise"
    )
  )
)

signals <- signals[order(-signals$horizon_scanning_profile), ]

clusters$cluster_priority <- round(clusters$coherence * clusters$strategic_concern, 4)
clusters <- clusters[order(-clusters$cluster_priority), ]

institutions$scanning_effectiveness_score <- round(
  0.20 * institutions$signal_strength -
  0.16 * institutions$ambiguity +
  0.24 * institutions$filtering_quality +
  0.22 * institutions$source_diversity +
  0.22 * institutions$institutional_uptake -
  0.16 * institutions$resistance,
  4
)

institutions <- institutions[order(-institutions$scanning_effectiveness_score), ]

write.csv(signals, file.path(outputs_dir, "r_horizon_signal_profiles.csv"), row.names = FALSE)
write.csv(clusters, file.path(outputs_dir, "r_signal_cluster_priorities.csv"), row.names = FALSE)
write.csv(institutions, file.path(outputs_dir, "r_institutional_scanning_effectiveness.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_horizon_signal_profiles.png"), width = 1200, height = 800)
barplot(
  signals$horizon_scanning_profile,
  names.arg = signals$signal_title,
  horiz = TRUE,
  las = 1,
  main = "Horizon Scanning Signal Profiles",
  xlab = "Profile score"
)
dev.off()

print(signals[, c("signal_title", "domain", "signal_type", "horizon_scanning_profile", "priority_class")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
