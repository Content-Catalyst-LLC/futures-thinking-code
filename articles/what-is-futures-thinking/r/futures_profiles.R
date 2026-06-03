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

profiles <- read.csv(file.path(data_dir, "practice_profiles.csv"))

weights <- c(
  predictive_emphasis = 0.05,
  uncertainty_plurality = 0.22,
  assumption_visibility = 0.18,
  participatory_depth = 0.15,
  strategic_readiness = 0.25,
  critical_reflection = 0.15
)

scores <- data.frame(
  practice = profiles$practice,
  anticipatory_capacity_score = numeric(nrow(profiles)),
  strongest_dimension = character(nrow(profiles)),
  weakest_dimension = character(nrow(profiles)),
  stringsAsFactors = FALSE
)

for (i in seq_len(nrow(profiles))) {
  vals <- as.numeric(profiles[i, names(weights)])
  names(vals) <- names(weights)
  scores$anticipatory_capacity_score[i] <- round(sum(vals * weights), 4)
  scores$strongest_dimension[i] <- names(vals)[which.max(vals)]
  scores$weakest_dimension[i] <- names(vals)[which.min(vals)]
}

scores <- scores[order(-scores$anticipatory_capacity_score), ]
write.csv(scores, file.path(outputs_dir, "r_practice_profile_scores.csv"), row.names = FALSE)
print(scores)
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
