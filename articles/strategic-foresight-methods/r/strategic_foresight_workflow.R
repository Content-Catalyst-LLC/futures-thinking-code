# Base R workflow for Strategic Foresight Methods.
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

methods <- read.csv(file.path(data_dir, "foresight_methods.csv"))
pipelines <- read.csv(file.path(data_dir, "pipeline_profiles.csv"))
signals <- read.csv(file.path(data_dir, "signals.csv"))

methods$method_profile_score <- round(
  0.16 * methods$detection_power +
  0.14 * methods$ambiguity_tolerance +
  0.16 * methods$structural_depth +
  0.18 * methods$actionability +
  0.14 * methods$participatory_depth +
  0.10 * methods$institutional_fit +
  0.12 * methods$learning_value,
  4
)

methods$method_risk_score <- round(
  methods$technocratic_risk *
  (1 - methods$participatory_depth) *
  (1 - methods$learning_value),
  4
)

methods <- methods[order(-methods$method_profile_score), ]

pipelines$method_gain <- round(
  0.14 * pipelines$detection +
  0.15 * pipelines$interpretation +
  0.14 * pipelines$pattern_formation +
  0.16 * pipelines$uncertainty_structuring +
  0.16 * pipelines$strategic_design +
  0.12 * pipelines$legitimacy +
  0.13 * pipelines$uptake,
  4
)

pipelines$actionable_foresight_score <- round(
  pipelines$method_gain +
  0.15 * pipelines$legitimacy +
  0.15 * pipelines$uptake -
  0.20 * pipelines$resistance,
  4
)

pipelines <- pipelines[order(-pipelines$actionable_foresight_score), ]

signals$watch_score <- round(
  0.35 * signals$uncertainty +
  0.40 * signals$impact +
  0.25 * signals$novelty,
  4
)

signals <- signals[order(-signals$watch_score), ]

write.csv(methods, file.path(outputs_dir, "r_foresight_method_profiles.csv"), row.names = FALSE)
write.csv(pipelines, file.path(outputs_dir, "r_pipeline_actionable_foresight_scores.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_signal_watch_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_foresight_method_profiles.png"), width = 1100, height = 700)
barplot(
  methods$method_profile_score,
  names.arg = methods$method,
  horiz = TRUE,
  las = 1,
  main = "Strategic Foresight Method Profiles",
  xlab = "Weighted profile score"
)
dev.off()

print(methods[, c("method", "primary_function", "method_profile_score", "method_risk_score")])
print(pipelines[, c("pipeline_name", "method_gain", "actionable_foresight_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
