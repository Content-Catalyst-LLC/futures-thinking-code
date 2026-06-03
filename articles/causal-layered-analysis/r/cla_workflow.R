# Base R workflow for Causal Layered Analysis.
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

issues <- read.csv(file.path(data_dir, "cla_issues.csv"))
layers <- read.csv(file.path(data_dir, "layer_codes.csv"))
reframes <- read.csv(file.path(data_dir, "reframing_profiles.csv"))

issues$cla_depth_score <- round(
  0.10 * issues$litany_visibility +
  0.18 * issues$systemic_explanation +
  0.22 * issues$worldview_challenge +
  0.20 * issues$myth_metaphor_depth +
  0.16 * issues$reframing_potential +
  0.08 * issues$power_sensitivity +
  0.06 * issues$strategic_relevance,
  4
)

issues$cla_class <- ifelse(
  issues$cla_depth_score >= 0.86,
  "High-depth reframing opportunity",
  ifelse(
    issues$cla_depth_score >= 0.80,
    "Strong layered analysis candidate",
    "Moderate CLA candidate"
  )
)

issues <- issues[order(-issues$cla_depth_score), ]

layers$layer_priority <- round(layers$diagnostic_weight * layers$transformation_need, 4)
layers <- layers[order(-layers$layer_priority), ]

reframes$reframing_depth_score <- round(
  0.12 * reframes$litany_change +
  0.20 * reframes$systemic_change +
  0.22 * reframes$worldview_change +
  0.22 * reframes$metaphor_change +
  0.12 * reframes$power_awareness +
  0.12 * reframes$strategic_coherence,
  4
)

reframes <- reframes[order(-reframes$reframing_depth_score), ]

write.csv(issues, file.path(outputs_dir, "r_cla_issue_depth_scores.csv"), row.names = FALSE)
write.csv(layers, file.path(outputs_dir, "r_layer_transformation_priorities.csv"), row.names = FALSE)
write.csv(reframes, file.path(outputs_dir, "r_reframing_depth_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_cla_issue_depth_scores.png"), width = 1200, height = 800)
barplot(
  issues$cla_depth_score,
  names.arg = issues$issue_title,
  horiz = TRUE,
  las = 1,
  main = "CLA Issue Depth Scores",
  xlab = "CLA depth score"
)
dev.off()

print(issues[, c("issue_title", "domain", "cla_depth_score", "cla_class")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
