# Base R workflow for Delphi Method and Expert Foresight.
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

responses <- read.csv(file.path(data_dir, "delphi_responses.csv"))
issues <- read.csv(file.path(data_dir, "issue_priorities.csv"))

responses$uncertainty_range <- responses$high_estimate - responses$low_estimate
responses$judgment_profile <- round(
  0.25 * responses$likelihood +
  0.35 * responses$impact +
  0.25 * responses$urgency +
  0.15 * responses$feasibility,
  4
)

round_keys <- unique(responses[, c("issue_id", "round")])
round_summary <- data.frame()

for (i in seq_len(nrow(round_keys))) {
  subset <- responses[
    responses$issue_id == round_keys$issue_id[i] &
    responses$round == round_keys$round[i],
  ]

  q <- quantile(subset$judgment_profile, probs = c(0.25, 0.75), names = FALSE)

  round_summary <- rbind(round_summary, data.frame(
    issue_id = round_keys$issue_id[i],
    round = round_keys$round[i],
    respondent_count = nrow(subset),
    median_judgment_profile = round(median(subset$judgment_profile), 4),
    mean_judgment_profile = round(mean(subset$judgment_profile), 4),
    lower_quartile = round(q[1], 4),
    upper_quartile = round(q[2], 4),
    interquartile_range = round(q[2] - q[1], 4),
    mean_uncertainty_range = round(mean(subset$uncertainty_range), 4)
  ))
}

issues$priority_score <- round(
  0.25 * issues$likelihood +
  0.30 * issues$impact +
  0.20 * issues$urgency +
  0.15 * issues$governance_relevance +
  0.10 * issues$monitoring_need,
  4
)

issues$uncertainty_adjusted_priority <- round(
  issues$priority_score * (1 + 0.20 * issues$uncertainty),
  4
)

issues <- issues[order(-issues$uncertainty_adjusted_priority), ]

write.csv(responses, file.path(outputs_dir, "r_expert_judgment_profiles.csv"), row.names = FALSE)
write.csv(round_summary, file.path(outputs_dir, "r_delphi_round_metrics.csv"), row.names = FALSE)
write.csv(issues, file.path(outputs_dir, "r_issue_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_issue_priority_scores.png"), width = 1200, height = 800)
barplot(
  issues$uncertainty_adjusted_priority,
  names.arg = issues$issue_title,
  horiz = TRUE,
  las = 1,
  main = "Delphi Issue Priority Scores",
  xlab = "Uncertainty-adjusted priority"
)
dev.off()

print(round_summary)
print(issues[, c("issue_title", "domain", "priority_score", "uncertainty_adjusted_priority")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
