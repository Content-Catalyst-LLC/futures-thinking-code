# Base R workflow for Uncertainty Matrices and Driver Mapping.
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

drivers <- read.csv(file.path(data_dir, "driver_register.csv"))
signals <- read.csv(file.path(data_dir, "signals.csv"))
assumptions <- read.csv(file.path(data_dir, "assumption_register.csv"))

drivers$driver_priority_score <- round(
  0.22 * drivers$impact +
  0.20 * drivers$uncertainty +
  0.14 * drivers$urgency +
  0.14 * drivers$interaction_strength +
  0.12 * drivers$distributional_burden +
  0.08 * drivers$monitoring_feasibility +
  0.06 * drivers$evidence_strength +
  0.04 * (1 - drivers$controllability),
  4
)

drivers$matrix_quadrant <- ifelse(
  drivers$impact >= 0.80 & drivers$uncertainty >= 0.72,
  "Critical uncertainty",
  ifelse(
    drivers$impact >= 0.80 & drivers$uncertainty < 0.72,
    "Baseline structural driver",
    ifelse(
      drivers$impact < 0.80 & drivers$uncertainty >= 0.72,
      "Watchlist uncertainty",
      "Lower-priority factor"
    )
  )
)

drivers$axis_suitability_score <- round(
  drivers$impact *
  drivers$uncertainty *
  drivers$interaction_strength *
  drivers$monitoring_feasibility *
  drivers$evidence_strength,
  4
)

drivers <- drivers[order(-drivers$driver_priority_score), ]

axis_candidates <- drivers[drivers$matrix_quadrant == "Critical uncertainty", ]
axis_candidates <- axis_candidates[order(-axis_candidates$axis_suitability_score), ]

signals$signal_priority_score <- round(
  0.15 * signals$novelty +
  0.30 * signals$relevance +
  0.25 * signals$urgency +
  0.15 * signals$evidence_quality +
  0.15 * signals$affected_voice,
  4
)
signals <- signals[order(-signals$signal_priority_score), ]

assumptions$assumption_failure_risk <- round(
  (1 - assumptions$confidence) * 0.45 + assumptions$fragility * 0.55,
  4
)
assumptions <- assumptions[order(-assumptions$assumption_failure_risk), ]

write.csv(drivers, file.path(outputs_dir, "r_driver_priority_scores.csv"), row.names = FALSE)
write.csv(axis_candidates, file.path(outputs_dir, "r_scenario_axis_candidates.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_signal_priority_scores.csv"), row.names = FALSE)
write.csv(assumptions, file.path(outputs_dir, "r_assumption_fragility_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_impact_uncertainty_matrix.png"), width = 1000, height = 800)
plot(
  drivers$uncertainty,
  drivers$impact,
  xlab = "Uncertainty",
  ylab = "Impact",
  main = "Impact-Uncertainty Matrix",
  pch = 19
)
text(drivers$uncertainty, drivers$impact, labels = drivers$driver_id, pos = 3, cex = 0.8)
abline(v = 0.72, lty = 2)
abline(h = 0.80, lty = 2)
dev.off()

png(file.path(outputs_dir, "r_driver_priority_scores.png"), width = 1200, height = 800)
barplot(
  drivers$driver_priority_score,
  names.arg = drivers$driver_name,
  horiz = TRUE,
  las = 1,
  main = "Driver Priority Scores",
  xlab = "Priority score"
)
dev.off()

print(drivers[, c("driver_id", "driver_name", "driver_priority_score", "matrix_quadrant")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
