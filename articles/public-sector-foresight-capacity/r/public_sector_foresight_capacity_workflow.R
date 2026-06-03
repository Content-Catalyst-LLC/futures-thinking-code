# Base R workflow for Public-Sector Foresight Capacity.
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

profiles <- read.csv(file.path(data_dir, "foresight_capacity_profiles.csv"))
signals <- read.csv(file.path(data_dir, "scanning_signals.csv"))
uptake <- read.csv(file.path(data_dir, "decision_uptake_register.csv"))

profiles$foresight_capacity_score <- round(
  0.12 * profiles$scanning_capacity +
  0.12 * profiles$scenario_capacity +
  0.14 * profiles$decision_uptake +
  0.12 * profiles$participation_capacity +
  0.12 * profiles$budget_connection +
  0.10 * profiles$evaluation_capacity +
  0.10 * profiles$institutional_learning +
  0.10 * profiles$implementation_authority +
  0.05 * profiles$knowledge_infrastructure +
  0.03 * profiles$legitimacy,
  4
)

profiles$capacity_gap_score <- round(
  0.16 * (1 - profiles$decision_uptake) +
  0.14 * (1 - profiles$budget_connection) +
  0.14 * (1 - profiles$implementation_authority) +
  0.12 * (1 - profiles$scanning_capacity) +
  0.12 * (1 - profiles$scenario_capacity) +
  0.10 * (1 - profiles$participation_capacity) +
  0.10 * (1 - profiles$evaluation_capacity) +
  0.08 * (1 - profiles$institutional_learning) +
  0.04 * (1 - profiles$knowledge_infrastructure),
  4
)

profiles <- profiles[order(-profiles$foresight_capacity_score), ]

signals$scanning_signal_priority_score <- round(
  0.16 * signals$signal_strength +
  0.12 * signals$novelty +
  0.12 * signals$uncertainty +
  0.18 * signals$policy_relevance +
  0.16 * signals$equity_relevance +
  0.12 * signals$detection_difficulty +
  0.14 * (1 - signals$response_readiness),
  4
)

signals$response_gap_score <- round(1 - signals$response_readiness, 4)
signals <- signals[order(-signals$scanning_signal_priority_score), ]

uptake$decision_uptake_score <- round(
  0.20 * uptake$uptake_strength +
  0.18 * uptake$budget_influence +
  0.14 * uptake$regulatory_influence +
  0.12 * uptake$procurement_influence +
  0.14 * uptake$implementation_influence +
  0.12 * uptake$evaluation_influence +
  0.10 * uptake$participation_influence,
  4
)

uptake <- uptake[order(-uptake$decision_uptake_score), ]

write.csv(profiles, file.path(outputs_dir, "r_foresight_capacity_scores.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_scanning_signal_scores.csv"), row.names = FALSE)
write.csv(uptake, file.path(outputs_dir, "r_decision_uptake_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_foresight_capacity_scores.png"), width = 1200, height = 800)
barplot(
  profiles$foresight_capacity_score,
  names.arg = profiles$foresight_model,
  horiz = TRUE,
  las = 1,
  main = "Public-Sector Foresight Capacity Scores",
  xlab = "Foresight capacity"
)
dev.off()

png(file.path(outputs_dir, "r_scanning_signal_priority_scores.png"), width = 1200, height = 800)
barplot(
  signals$scanning_signal_priority_score,
  names.arg = signals$signal_name,
  horiz = TRUE,
  las = 1,
  main = "Scanning Signal Priority Scores",
  xlab = "Signal priority"
)
dev.off()

print(profiles[, c("capacity_id", "foresight_model", "foresight_capacity_score", "capacity_gap_score")])
print(signals[, c("signal_id", "signal_name", "scanning_signal_priority_score", "response_gap_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
