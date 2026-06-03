# Base R workflow for Law, Regulation, and Emerging Futures.
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

models <- read.csv(file.path(data_dir, "regulatory_models.csv"))
risks <- read.csv(file.path(data_dir, "emerging_risk_register.csv"))
rights <- read.csv(file.path(data_dir, "rights_remedy_register.csv"))

models$future_ready_regulatory_capacity_score <- round(
  0.13 * models$foresight_capacity +
  0.12 * models$monitoring_capacity +
  0.12 * models$enforcement_capacity +
  0.14 * models$rights_protection +
  0.10 * models$public_participation +
  0.12 * models$revision_authority +
  0.10 * models$regulatory_learning +
  0.08 * models$capture_resistance +
  0.05 * models$legal_certainty +
  0.04 * models$remedy_access,
  4
)

models$regulatory_lag_pressure_score <- round(
  0.16 * (1 - models$foresight_capacity) +
  0.14 * (1 - models$monitoring_capacity) +
  0.14 * (1 - models$revision_authority) +
  0.12 * (1 - models$regulatory_learning) +
  0.12 * (1 - models$enforcement_capacity) +
  0.10 * (1 - models$rights_protection) +
  0.08 * (1 - models$public_participation) +
  0.08 * (1 - models$capture_resistance) +
  0.06 * (1 - models$remedy_access),
  4
)

models <- models[order(-models$future_ready_regulatory_capacity_score), ]

risks$emerging_regulatory_risk_score <- round(
  0.16 * risks$change_velocity +
  0.18 * risks$harm_severity +
  0.13 * risks$uncertainty +
  0.15 * risks$irreversibility +
  0.15 * risks$distributional_exposure +
  0.15 * risks$regulatory_gap +
  0.08 * (1 - risks$mitigation_capacity),
  4
)

risks <- risks[order(-risks$emerging_regulatory_risk_score), ]

rights$rights_remedy_strength_score <- round(
  0.14 * rights$notice +
  0.14 * rights$explanation +
  0.15 * rights$appeal +
  0.15 * rights$audit_access +
  0.14 * rights$public_enforcement +
  0.12 * rights$collective_remedy +
  0.08 * rights$compensation +
  0.08 * rights$accessibility,
  4
)

rights <- rights[order(-rights$rights_remedy_strength_score), ]

write.csv(models, file.path(outputs_dir, "r_regulatory_model_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_emerging_risk_scores.csv"), row.names = FALSE)
write.csv(rights, file.path(outputs_dir, "r_rights_remedy_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_regulatory_capacity_scores.png"), width = 1200, height = 800)
barplot(
  models$future_ready_regulatory_capacity_score,
  names.arg = models$regulatory_model,
  horiz = TRUE,
  las = 1,
  main = "Future-Ready Regulatory Capacity Scores",
  xlab = "Capacity score"
)
dev.off()

png(file.path(outputs_dir, "r_regulatory_lag_pressure_scores.png"), width = 1200, height = 800)
barplot(
  models$regulatory_lag_pressure_score,
  names.arg = models$regulatory_model,
  horiz = TRUE,
  las = 1,
  main = "Regulatory Lag Pressure Scores",
  xlab = "Lag pressure"
)
dev.off()

print(models[, c("model_id", "regulatory_model", "future_ready_regulatory_capacity_score", "regulatory_lag_pressure_score")])
print(risks[, c("risk_id", "risk_name", "emerging_regulatory_risk_score", "mitigation_capacity")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
