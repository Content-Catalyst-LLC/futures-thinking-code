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

profiles <- read.csv(file.path(data_dir, "geopolitical_futures_profiles.csv"))

profiles$geopolitical_stability_score <- round(
  0.11 * (1 - profiles$power_concentration) +
  0.10 * profiles$interdependence +
  0.16 * profiles$institutional_coordination -
  0.12 * profiles$technological_competition -
  0.12 * profiles$climate_stress -
  0.11 * profiles$economic_vulnerability +
  0.12 * profiles$domestic_resilience +
  0.11 * profiles$information_integrity +
  0.08 * profiles$resource_security +
  0.07 * profiles$crisis_communication,
  4
)

profiles$cascade_risk_score <- round(
  0.12 * profiles$power_concentration +
  0.13 * profiles$technological_competition +
  0.14 * profiles$climate_stress +
  0.13 * profiles$economic_vulnerability +
  0.11 * (1 - profiles$institutional_coordination) +
  0.10 * (1 - profiles$domestic_resilience) +
  0.10 * (1 - profiles$information_integrity) +
  0.09 * (1 - profiles$resource_security) +
  0.08 * (1 - profiles$crisis_communication),
  4
)

profiles <- profiles[order(-profiles$geopolitical_stability_score), ]
write.csv(profiles, file.path(outputs_dir, "r_geopolitical_profile_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_geopolitical_stability_scores.png"), width = 1200, height = 800)
barplot(profiles$geopolitical_stability_score, names.arg = profiles$future_name, horiz = TRUE, las = 1, main = "Geopolitical Stability Scores", xlab = "Stability score")
dev.off()

print(profiles[, c("profile_id", "future_name", "geopolitical_stability_score", "cascade_risk_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
