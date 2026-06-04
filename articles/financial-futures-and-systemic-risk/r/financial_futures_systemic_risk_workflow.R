# Base R workflow for Financial Futures and Systemic Risk.
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

profiles <- read.csv(file.path(data_dir, "financial_system_profiles.csv"))
policies <- read.csv(file.path(data_dir, "policy_options.csv"))
risks <- read.csv(file.path(data_dir, "risk_indicators.csv"))

profiles$financial_resilience_score <- round(
  0.14 * profiles$liquidity_resilience +
  0.14 * profiles$household_security +
  0.14 * profiles$regulatory_strength +
  0.10 * profiles$public_finance_capacity +
  0.10 * profiles$consumer_protection +
  0.10 * profiles$productive_investment +
  0.10 * (1 - profiles$leverage) +
  0.08 * (1 - profiles$climate_exposure) +
  0.06 * (1 - profiles$nonbank_exposure) +
  0.04 * (1 - profiles$digital_run_risk),
  4
)

profiles$systemic_risk_score <- round(
  0.16 * profiles$leverage +
  0.14 * (1 - profiles$liquidity_resilience) +
  0.14 * profiles$climate_exposure +
  0.13 * profiles$nonbank_exposure +
  0.13 * profiles$digital_run_risk +
  0.12 * (1 - profiles$household_security) +
  0.10 * (1 - profiles$public_finance_capacity) +
  0.08 * (1 - profiles$regulatory_strength),
  4
)

profiles <- profiles[order(-profiles$financial_resilience_score), ]

policies$financial_stability_gain_score <- round(
  0.16 * policies$capital_buffer_strength +
  0.16 * policies$liquidity_support +
  0.14 * policies$consumer_protection_gain +
  0.14 * policies$climate_risk_governance +
  0.14 * policies$nonbank_oversight +
  0.12 * policies$digital_resilience +
  0.10 * policies$public_finance_support +
  0.04 * policies$implementation_capacity,
  4
)

policies <- policies[order(-policies$financial_stability_gain_score), ]

risks$systemic_risk_priority_score <- round(
  0.15 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$contagion_potential +
  0.14 * risks$opacity +
  0.14 * risks$recovery_difficulty +
  0.14 * risks$distributional_harm +
  0.08 * (1 - risks$policy_preparedness),
  4
)

risks <- risks[order(-risks$systemic_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_financial_profile_scores.csv"), row.names = FALSE)
write.csv(policies, file.path(outputs_dir, "r_policy_option_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_risk_indicator_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_financial_resilience_scores.png"), width = 1200, height = 800)
barplot(
  profiles$financial_resilience_score,
  names.arg = profiles$financial_future_name,
  horiz = TRUE,
  las = 1,
  main = "Financial Resilience Scores",
  xlab = "Resilience score"
)
dev.off()

png(file.path(outputs_dir, "r_systemic_risk_scores.png"), width = 1200, height = 800)
barplot(
  profiles$systemic_risk_score,
  names.arg = profiles$financial_future_name,
  horiz = TRUE,
  las = 1,
  main = "Systemic Risk Scores",
  xlab = "Risk score"
)
dev.off()

print(profiles[, c("profile_id", "financial_future_name", "financial_resilience_score", "systemic_risk_score")])
print(policies[, c("policy_id", "policy_name", "financial_stability_gain_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
