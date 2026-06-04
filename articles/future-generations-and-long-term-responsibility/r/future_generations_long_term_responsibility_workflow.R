# Base R workflow for Future Generations and Long-Term Responsibility.
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

profiles <- read.csv(file.path(data_dir, "intergenerational_responsibility_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "intergenerational_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "long_term_risk_indicators.csv"))
records <- read.csv(file.path(data_dir, "inheritance_records.csv"))

profiles$inherited_burden_score <- round(
  0.18 * profiles$climate_burden +
  0.14 * profiles$debt_without_assets +
  0.16 * profiles$infrastructure_decay +
  0.18 * profiles$ecological_damage +
  0.14 * profiles$technological_lock_in +
  0.10 * (1 - profiles$institutional_capacity) +
  0.06 * (1 - profiles$adaptive_capacity) +
  0.04 * (1 - profiles$future_representation),
  4
)

profiles$future_freedom_score <- round(
  0.20 * profiles$institutional_capacity +
  0.20 * profiles$adaptive_capacity +
  0.16 * profiles$future_representation +
  0.14 * (1 - profiles$technological_lock_in) +
  0.12 * (1 - profiles$infrastructure_decay) +
  0.10 * (1 - profiles$ecological_damage) +
  0.05 * (1 - profiles$climate_burden) +
  0.03 * (1 - profiles$debt_without_assets),
  4
)

profiles$stewardship_score <- round(
  0.18 * profiles$future_freedom_score +
  0.18 * profiles$institutional_capacity +
  0.18 * profiles$adaptive_capacity +
  0.14 * profiles$future_representation +
  0.12 * profiles$reparative_continuity +
  0.10 * profiles$public_legitimacy -
  0.06 * profiles$inherited_burden_score -
  0.04 * profiles$ecological_damage,
  4
)

profiles <- profiles[order(-profiles$stewardship_score), ]

strategies$intergenerational_strategy_value_score <- round(
  0.13 * strategies$future_generation_review_gain +
  0.13 * strategies$climate_budgeting_gain +
  0.12 * strategies$maintenance_accounting_gain +
  0.12 * strategies$ecological_restoration_gain +
  0.11 * strategies$public_investment_gain +
  0.10 * strategies$youth_participation_gain +
  0.10 * strategies$technology_accountability_gain +
  0.09 * strategies$reparative_finance_gain +
  0.07 * strategies$adaptive_governance_gain +
  0.02 * strategies$implementation_capacity +
  0.01 * strategies$public_legitimacy_gain,
  4
)

strategies <- strategies[order(-strategies$intergenerational_strategy_value_score), ]

risks$long_term_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.16 * risks$severity +
  0.15 * risks$irreversibility +
  0.10 * risks$visibility_gap +
  0.18 * risks$distributional_harm +
  0.18 * risks$future_generation_harm +
  0.09 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$long_term_risk_priority_score), ]

records$stewardship_capacity_score <- round(
  0.18 * records$future_freedom +
  0.18 * records$institutional_capacity +
  0.18 * records$adaptive_capacity +
  0.14 * records$future_representation +
  0.12 * records$reparative_continuity +
  0.10 * records$public_legitimacy -
  0.06 * records$inherited_burden -
  0.04 * records$ecological_damage,
  4
)

records$burden_gap_score <- round(pmax(
  0,
  records$inherited_burden + records$ecological_damage - records$future_freedom - records$adaptive_capacity
), 4)

records <- records[order(-records$stewardship_capacity_score), ]

write.csv(profiles, file.path(outputs_dir, "r_intergenerational_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_intergenerational_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_long_term_risk_priority_scores.csv"), row.names = FALSE)
write.csv(records, file.path(outputs_dir, "r_inheritance_record_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_stewardship_scores.png"), width = 1200, height = 800)
barplot(
  profiles$stewardship_score,
  names.arg = profiles$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Long-Term Stewardship Scores",
  xlab = "Stewardship score"
)
dev.off()

png(file.path(outputs_dir, "r_inherited_burden_scores.png"), width = 1200, height = 800)
barplot(
  profiles$inherited_burden_score,
  names.arg = profiles$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Inherited Burden Scores",
  xlab = "Inherited burden"
)
dev.off()

print(profiles[, c("profile_id", "scenario_name", "inherited_burden_score", "future_freedom_score", "stewardship_score")])
print(strategies[, c("strategy_id", "strategy_name", "intergenerational_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
