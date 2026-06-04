# Base R workflow for Colonial Futures and Contested Imagination.
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

profiles <- read.csv(file.path(data_dir, "colonial_future_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "reparative_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "coloniality_risk_indicators.csv"))
records <- read.csv(file.path(data_dir, "extraction_voice_records.csv"))

profiles$coloniality_risk_score <- round(
  0.12 * profiles$agenda_setting_power +
  0.12 * (1 - profiles$consent_quality) +
  0.12 * profiles$land_exposure +
  0.12 * profiles$external_control +
  0.11 * (1 - profiles$epistemic_justice) +
  0.10 * (1 - profiles$local_benefit) +
  0.10 * profiles$ecological_harm +
  0.09 * (1 - profiles$reparative_capacity) +
  0.07 * (1 - profiles$sovereignty_recognition) +
  0.03 * (1 - profiles$data_sovereignty) +
  0.02 * (1 - profiles$labor_protection),
  4
)

profiles$reparative_future_score <- round(
  0.16 * profiles$consent_quality +
  0.15 * profiles$epistemic_justice +
  0.14 * profiles$local_benefit +
  0.16 * profiles$reparative_capacity +
  0.14 * profiles$sovereignty_recognition +
  0.08 * profiles$data_sovereignty +
  0.07 * profiles$labor_protection +
  0.05 * (1 - profiles$external_control) +
  0.03 * (1 - profiles$land_exposure) +
  0.02 * (1 - profiles$ecological_harm),
  4
)

profiles$reparative_gap_score <- pmax(0, profiles$coloniality_risk_score - profiles$reparative_future_score)
profiles <- profiles[order(-profiles$coloniality_risk_score), ]

strategies$reparative_strategy_value_score <- round(
  0.13 * strategies$land_return_gain +
  0.13 * strategies$consent_quality_gain +
  0.12 * strategies$community_ownership_gain +
  0.12 * strategies$epistemic_justice_gain +
  0.10 * strategies$data_sovereignty_gain +
  0.10 * strategies$labor_rights_gain +
  0.10 * strategies$ecological_restoration_gain +
  0.09 * strategies$reparative_finance_gain +
  0.07 * strategies$accountability_gain +
  0.02 * strategies$implementation_capacity +
  0.02 * strategies$legitimacy_gain,
  4
)

strategies <- strategies[order(-strategies$reparative_strategy_value_score), ]

risks$coloniality_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.17 * risks$severity +
  0.15 * risks$irreversibility +
  0.10 * risks$visibility_gap +
  0.20 * risks$distributional_harm +
  0.14 * risks$rights_risk +
  0.10 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$coloniality_risk_priority_score), ]

records$future_making_legitimacy_score <- round(
  0.18 * records$community_voice +
  0.16 * records$local_benefit +
  0.16 * records$reparative_capacity +
  0.16 * records$consent_quality +
  0.14 * records$sovereignty_recognition -
  0.08 * records$extraction_burden -
  0.07 * records$external_control -
  0.05 * records$ecological_harm,
  4
)

records$reparative_gap_score <- round(pmax(
  0,
  records$extraction_burden + records$external_control + records$ecological_harm -
  records$local_benefit - records$reparative_capacity - records$consent_quality
), 4)

records <- records[order(-records$reparative_gap_score), ]

write.csv(profiles, file.path(outputs_dir, "r_colonial_future_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_reparative_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_coloniality_risk_priority_scores.csv"), row.names = FALSE)
write.csv(records, file.path(outputs_dir, "r_extraction_voice_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_coloniality_risk_scores.png"), width = 1200, height = 800)
barplot(
  profiles$coloniality_risk_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Coloniality Risk Scores",
  xlab = "Coloniality risk score"
)
dev.off()

png(file.path(outputs_dir, "r_reparative_future_scores.png"), width = 1200, height = 800)
barplot(
  profiles$reparative_future_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Reparative Future Scores",
  xlab = "Reparative future score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "coloniality_risk_score", "reparative_future_score", "reparative_gap_score")])
print(strategies[, c("strategy_id", "strategy_name", "reparative_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
