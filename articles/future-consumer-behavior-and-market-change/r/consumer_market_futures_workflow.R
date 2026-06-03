# Base R workflow for Future Consumer Behavior and Market Change.
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

profiles <- read.csv(file.path(data_dir, "consumer_future_profiles.csv"))
options <- read.csv(file.path(data_dir, "consumer_strategy_options.csv"))
vulnerabilities <- read.csv(file.path(data_dir, "vulnerability_indicators.csv"))

profiles$consumer_future_health_score <- round(
  0.14 * profiles$affordability +
  0.16 * profiles$trust +
  0.10 * profiles$sustainability_demand +
  0.16 * profiles$access_inclusion +
  0.10 * (1 - profiles$price_sensitivity) +
  0.12 * (1 - profiles$behavioral_friction) +
  0.06 * profiles$digital_dependence +
  0.06 * profiles$regulatory_pressure +
  0.06 * profiles$privacy_confidence +
  0.04 * profiles$local_resilience,
  4
)

profiles$market_fragility_score <- round(
  0.16 * profiles$price_sensitivity +
  0.16 * profiles$behavioral_friction +
  0.14 * (1 - profiles$trust) +
  0.12 * (1 - profiles$access_inclusion) +
  0.10 * (1 - profiles$affordability) +
  0.10 * profiles$digital_dependence +
  0.08 * (1 - profiles$privacy_confidence) +
  0.08 * (1 - profiles$local_resilience) +
  0.06 * profiles$regulatory_pressure,
  4
)

profiles <- profiles[order(-profiles$consumer_future_health_score), ]

options$consumer_support_strategy_score <- round(
  0.16 * options$affordability_support +
  0.16 * options$trust_building +
  0.14 * options$privacy_protection +
  0.14 * options$access_inclusion +
  0.14 * options$sustainability_credibility +
  0.14 * options$behavioral_integrity +
  0.06 * options$implementation_capacity +
  0.06 * options$market_scalability,
  4
)

options <- options[order(-options$consumer_support_strategy_score), ]

vulnerabilities$consumer_vulnerability_priority_score <- round(
  0.18 * vulnerabilities$budget_pressure +
  0.16 * vulnerabilities$information_asymmetry +
  0.14 * vulnerabilities$digital_exclusion +
  0.18 * vulnerabilities$behavioral_manipulation +
  0.14 * vulnerabilities$lack_of_alternatives +
  0.10 * (1 - vulnerabilities$remedy_access) +
  0.10 * (1 - vulnerabilities$consumer_protection),
  4
)

vulnerabilities <- vulnerabilities[order(-vulnerabilities$consumer_vulnerability_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_consumer_future_profile_scores.csv"), row.names = FALSE)
write.csv(options, file.path(outputs_dir, "r_consumer_strategy_option_scores.csv"), row.names = FALSE)
write.csv(vulnerabilities, file.path(outputs_dir, "r_vulnerability_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_consumer_future_health_scores.png"), width = 1200, height = 800)
barplot(
  profiles$consumer_future_health_score,
  names.arg = profiles$consumer_future_name,
  horiz = TRUE,
  las = 1,
  main = "Consumer Future Health Scores",
  xlab = "Health score"
)
dev.off()

png(file.path(outputs_dir, "r_market_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$market_fragility_score,
  names.arg = profiles$consumer_future_name,
  horiz = TRUE,
  las = 1,
  main = "Market Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "consumer_future_name", "consumer_future_health_score", "market_fragility_score")])
print(options[, c("option_id", "option_name", "consumer_support_strategy_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
