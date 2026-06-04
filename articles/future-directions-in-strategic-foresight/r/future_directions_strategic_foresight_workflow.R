# Base R workflow for Future Directions in Strategic Foresight.
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

profiles <- read.csv(file.path(data_dir, "foresight_capability_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "foresight_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "foresight_risk_indicators.csv"))
signals <- read.csv(file.path(data_dir, "foresight_signal_records.csv"))

profiles$foresight_capability_score <- round(
  0.16 * profiles$signal_detection +
  0.16 * profiles$scenario_capability +
  0.14 * profiles$learning_capacity +
  0.14 * profiles$governance_integration +
  0.12 * profiles$adaptive_flexibility +
  0.10 * profiles$participatory_legitimacy +
  0.10 * profiles$ethical_accountability +
  0.08 * profiles$data_infrastructure,
  4
)

profiles$technical_capability_score <- round(
  0.35 * profiles$signal_detection +
  0.35 * profiles$scenario_capability +
  0.30 * profiles$data_infrastructure,
  4
)

profiles$governance_capability_score <- round(
  0.45 * profiles$governance_integration +
  0.30 * profiles$adaptive_flexibility +
  0.25 * profiles$learning_capacity,
  4
)

profiles$legitimacy_capability_score <- round(
  0.40 * profiles$participatory_legitimacy +
  0.35 * profiles$ethical_accountability +
  0.25 * profiles$public_legitimacy,
  4
)

profiles$capability_gap_score <- round(pmax(
  0,
  profiles$technical_capability_score -
  ((profiles$governance_capability_score + profiles$legitimacy_capability_score) / 2)
), 4)

profiles <- profiles[order(-profiles$foresight_capability_score), ]

strategies$foresight_capability_gain_score <- round(
  0.11 * strategies$signal_pipeline_gain +
  0.12 * strategies$scenario_update_gain +
  0.14 * strategies$governance_integration_gain +
  0.10 * strategies$data_system_gain +
  0.11 * strategies$participatory_legitimacy_gain +
  0.11 * strategies$ethical_accountability_gain +
  0.12 * strategies$adaptive_strategy_gain +
  0.07 * strategies$ai_audit_gain +
  0.08 * strategies$learning_capacity_gain +
  0.02 * strategies$implementation_capacity +
  0.02 * strategies$public_legitimacy_gain,
  4
)

strategies <- strategies[order(-strategies$foresight_capability_gain_score), ]

risks$foresight_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.17 * risks$severity +
  0.12 * risks$irreversibility +
  0.12 * risks$visibility_gap +
  0.18 * risks$governance_gap +
  0.17 * risks$legitimacy_gap +
  0.10 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$foresight_risk_priority_score), ]

signals$strategic_attention_score <- round(
  0.16 * signals$signal_strength +
  0.14 * signals$signal_velocity +
  0.10 * signals$novelty +
  0.20 * signals$relevance +
  0.14 * signals$source_quality +
  0.14 * signals$interpretive_confidence +
  0.12 * signals$uncertainty,
  4
)

signals$ambiguity_score <- round(signals$uncertainty * (1 - signals$interpretive_confidence), 4)
signals <- signals[order(-signals$strategic_attention_score), ]

write.csv(profiles, file.path(outputs_dir, "r_foresight_capability_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_foresight_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_foresight_risk_priority_scores.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_foresight_signal_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_foresight_capability_scores.png"), width = 1200, height = 800)
barplot(
  profiles$foresight_capability_score,
  names.arg = profiles$institution_type,
  horiz = TRUE,
  las = 1,
  main = "Integrated Foresight Capability Scores",
  xlab = "Foresight capability score"
)
dev.off()

png(file.path(outputs_dir, "r_capability_gap_scores.png"), width = 1200, height = 800)
barplot(
  profiles$capability_gap_score,
  names.arg = profiles$institution_type,
  horiz = TRUE,
  las = 1,
  main = "Foresight Capability Gap Scores",
  xlab = "Capability gap score"
)
dev.off()

print(profiles[, c("institution_id", "institution_type", "foresight_capability_score", "technical_capability_score", "governance_capability_score", "legitimacy_capability_score", "capability_gap_score")])
print(strategies[, c("strategy_id", "strategy_name", "foresight_capability_gain_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
