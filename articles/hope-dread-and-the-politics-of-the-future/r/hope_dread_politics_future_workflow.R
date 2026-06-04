# Base R workflow for Hope, Dread, and the Politics of the Future.
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

profiles <- read.csv(file.path(data_dir, "future_emotion_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "future_emotion_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "future_emotion_risk_indicators.csv"))
records <- read.csv(file.path(data_dir, "future_emotion_records.csv"))

profiles$mobilization_score <- round(profiles$agency * (profiles$hope + 0.55 * profiles$dread) * profiles$trust, 4)
profiles$paralysis_risk_score <- round(profiles$dread * (1 - profiles$agency) * (1 - profiles$trust), 4)

profiles$disciplined_hope_score <- round(
  0.18 * profiles$hope +
  0.18 * profiles$agency +
  0.16 * profiles$trust +
  0.16 * profiles$institutional_capacity +
  0.14 * profiles$narrative_accountability +
  0.12 * profiles$repair_capacity -
  0.04 * profiles$future_fatigue -
  0.02 * profiles$polarization,
  4
)

profiles$fear_politics_risk_score <- round(
  0.24 * profiles$dread +
  0.22 * profiles$polarization +
  0.18 * (1 - profiles$trust) +
  0.16 * (1 - profiles$agency) +
  0.12 * profiles$future_fatigue +
  0.08 * (1 - profiles$narrative_accountability),
  4
)

profiles <- profiles[order(-profiles$disciplined_hope_score), ]

strategies$future_emotion_strategy_value_score <- round(
  0.13 * strategies$agency_pathway_gain +
  0.12 * strategies$trust_repair_gain +
  0.13 * strategies$narrative_accountability_gain +
  0.11 * strategies$participatory_foresight_gain +
  0.11 * strategies$climate_truth_action_gain +
  0.10 * strategies$youth_representation_gain +
  0.08 * strategies$media_literacy_gain +
  0.10 * strategies$repair_capacity_gain +
  0.08 * strategies$fear_politics_resistance_gain +
  0.02 * strategies$implementation_capacity +
  0.02 * strategies$public_legitimacy_gain,
  4
)

strategies <- strategies[order(-strategies$future_emotion_strategy_value_score), ]

risks$future_emotion_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.16 * risks$severity +
  0.12 * risks$irreversibility +
  0.12 * risks$visibility_gap +
  0.16 * risks$distributional_harm +
  0.20 * risks$democratic_harm +
  0.10 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$future_emotion_risk_priority_score), ]

records$mobilization_score <- round(records$agency * (records$hope + 0.55 * records$dread) * records$trust, 4)
records$paralysis_risk_score <- round(records$dread * (1 - records$agency) * (1 - records$trust), 4)

records$disciplined_hope_score <- round(
  0.22 * records$hope +
  0.22 * records$agency +
  0.18 * records$trust +
  0.18 * records$repair_capacity +
  0.12 * records$narrative_accountability -
  0.05 * records$future_fatigue -
  0.03 * records$polarization,
  4
)

records$false_hope_risk_score <- round(pmax(0, records$hope - records$narrative_accountability - records$repair_capacity), 4)

records <- records[order(-records$disciplined_hope_score), ]

write.csv(profiles, file.path(outputs_dir, "r_future_emotion_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_future_emotion_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_future_emotion_risk_priority_scores.csv"), row.names = FALSE)
write.csv(records, file.path(outputs_dir, "r_future_emotion_record_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_disciplined_hope_scores.png"), width = 1200, height = 800)
barplot(
  profiles$disciplined_hope_score,
  names.arg = profiles$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Disciplined Hope Scores",
  xlab = "Disciplined hope score"
)
dev.off()

png(file.path(outputs_dir, "r_fear_politics_risk_scores.png"), width = 1200, height = 800)
barplot(
  profiles$fear_politics_risk_score,
  names.arg = profiles$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Fear-Politics Risk Scores",
  xlab = "Fear-politics risk score"
)
dev.off()

print(profiles[, c("profile_id", "scenario_name", "mobilization_score", "paralysis_risk_score", "disciplined_hope_score", "fear_politics_risk_score")])
print(strategies[, c("strategy_id", "strategy_name", "future_emotion_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
