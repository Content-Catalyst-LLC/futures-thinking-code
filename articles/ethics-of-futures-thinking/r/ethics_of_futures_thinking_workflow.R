# Base R workflow for Ethics of Futures Thinking.
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

profiles <- read.csv(file.path(data_dir, "ethical_futures_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "ethical_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "ethical_risk_indicators.csv"))
distribution <- read.csv(file.path(data_dir, "stakeholder_distribution_paths.csv"))

profiles$ethical_futures_profile_score <- round(
  0.13 * profiles$intergenerational_responsibility +
  0.12 * profiles$inclusion +
  0.12 * profiles$accountability +
  0.12 * profiles$risk_equity +
  0.10 * profiles$transparency +
  0.10 * profiles$contestability +
  0.10 * profiles$precaution +
  0.08 * profiles$adaptive_learning +
  0.08 * profiles$epistemic_pluralism +
  0.05 * profiles$public_legitimacy,
  4
)

profiles$ethical_capacity_gap <- round(1 - profiles$ethical_futures_profile_score, 4)
profiles <- profiles[order(-profiles$ethical_futures_profile_score), ]

strategies$ethical_strategy_value_score <- round(
  0.11 * strategies$value_transparency_gain +
  0.13 * strategies$participation_gain +
  0.13 * strategies$distributional_justice_gain +
  0.12 * strategies$intergenerational_review_gain +
  0.10 * strategies$epistemic_pluralism_gain +
  0.09 * strategies$precaution_gain +
  0.11 * strategies$accountability_gain +
  0.10 * strategies$contestability_gain +
  0.07 * strategies$adaptive_learning_gain +
  0.02 * strategies$implementation_capacity +
  0.02 * strategies$public_legitimacy_gain,
  4
)

strategies <- strategies[order(-strategies$ethical_strategy_value_score), ]

risks$ethical_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.17 * risks$severity +
  0.15 * risks$irreversibility +
  0.10 * risks$visibility_gap +
  0.20 * risks$distributional_harm +
  0.14 * risks$rights_risk +
  0.10 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$ethical_risk_priority_score), ]

distribution$net_welfare <- distribution$benefit - distribution$risk
distribution$justice_adjusted_score <- round(
  distribution$benefit -
  distribution$risk -
  0.35 * distribution$exposure +
  0.25 * distribution$protection +
  0.20 * distribution$moral_weight +
  0.10 * distribution$voice_weight,
  4
)

distribution <- distribution[order(distribution$justice_adjusted_score), ]

write.csv(profiles, file.path(outputs_dir, "r_ethical_futures_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_ethical_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_ethical_risk_priority_scores.csv"), row.names = FALSE)
write.csv(distribution, file.path(outputs_dir, "r_stakeholder_distribution_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_ethical_futures_profile_scores.png"), width = 1200, height = 800)
barplot(
  profiles$ethical_futures_profile_score,
  names.arg = profiles$institution_type,
  horiz = TRUE,
  las = 1,
  main = "Ethical Futures Profile Scores",
  xlab = "Profile score"
)
dev.off()

png(file.path(outputs_dir, "r_stakeholder_justice_scores.png"), width = 1200, height = 800)
avg_scores <- aggregate(justice_adjusted_score ~ group_name, data = distribution, FUN = mean)
avg_scores <- avg_scores[order(avg_scores$justice_adjusted_score), ]
barplot(
  avg_scores$justice_adjusted_score,
  names.arg = avg_scores$group_name,
  horiz = TRUE,
  las = 1,
  main = "Mean Justice-Adjusted Stakeholder Scores",
  xlab = "Justice-adjusted score"
)
dev.off()

print(profiles[, c("profile_id", "institution_type", "ethical_futures_profile_score", "ethical_capacity_gap")])
print(strategies[, c("strategy_id", "strategy_name", "ethical_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
