# Base R workflow for Early Warning Systems and Futures Intelligence.
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
indicators <- read.csv(file.path(data_dir, "indicators.csv"))
assumptions <- read.csv(file.path(data_dir, "assumptions.csv"))

signals$warning_score <- round(
  0.12 * signals$novelty +
  0.22 * signals$relevance +
  0.20 * signals$urgency +
  0.13 * signals$evidence_quality +
  0.11 * signals$affected_voice +
  0.13 * signals$vulnerability +
  0.09 * signals$lead_time_value,
  4
)

signals$warning_level <- ifelse(
  signals$warning_score >= 0.82,
  "Escalate",
  ifelse(signals$warning_score >= 0.76, "Watch closely", "Monitor")
)

signals <- signals[order(-signals$warning_score), ]

review_weight <- function(freq) {
  ifelse(freq == "monthly", 1.00,
    ifelse(freq == "quarterly", 0.88,
      ifelse(freq == "semiannual", 0.68,
        ifelse(freq == "annual", 0.48, 0.50)
      )
    )
  )
}

indicators$threshold_gap <- indicators$current_value - indicators$threshold_value
indicators$threshold_breached <- indicators$current_value >= indicators$threshold_value
indicators$review_weight <- review_weight(indicators$review_frequency)
indicators$positive_gap <- pmax(0, indicators$threshold_gap)
indicators$trigger_priority_score <- round(
  0.45 * as.numeric(indicators$threshold_breached) +
  0.25 * indicators$current_value +
  0.20 * indicators$positive_gap +
  0.10 * indicators$review_weight,
  4
)

indicators <- indicators[order(-indicators$trigger_priority_score), ]

assumptions$assumption_failure_risk <- round(
  0.45 * (1 - assumptions$confidence) +
  0.55 * assumptions$fragility,
  4
)

assumptions <- assumptions[order(-assumptions$assumption_failure_risk), ]

write.csv(signals, file.path(outputs_dir, "r_signal_warning_scores.csv"), row.names = FALSE)
write.csv(indicators, file.path(outputs_dir, "r_threshold_trigger_scores.csv"), row.names = FALSE)
write.csv(assumptions, file.path(outputs_dir, "r_assumption_failure_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_signal_warning_scores.png"), width = 1200, height = 800)
barplot(
  signals$warning_score,
  names.arg = signals$signal_name,
  horiz = TRUE,
  las = 1,
  main = "Early Warning Signal Scores",
  xlab = "Warning score"
)
dev.off()

print(signals[, c("signal_id", "signal_name", "warning_score", "warning_level")])
print(indicators[, c("indicator_id", "indicator_name", "current_value", "threshold_value", "threshold_breached", "trigger_priority_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
