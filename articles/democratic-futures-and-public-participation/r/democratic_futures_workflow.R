# Base R workflow for Democratic Futures and Public Participation.
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

models <- read.csv(file.path(data_dir, "participation_models.csv"))
representation <- read.csv(file.path(data_dir, "representation_profiles.csv"))
uptake <- read.csv(file.path(data_dir, "decision_uptake_register.csv"))

models$democratic_futures_capacity_score <- round(
  0.11 * models$inclusion +
  0.12 * models$deliberative_quality +
  0.11 * models$representation +
  0.14 * models$institutional_uptake +
  0.12 * models$accountability +
  0.12 * models$justice_safeguards +
  0.08 * models$public_learning +
  0.10 * models$decision_influence +
  0.05 * models$accessibility +
  0.05 * models$community_authority,
  4
)

models$tokenism_risk_score <- round(
  0.18 * (1 - models$institutional_uptake) +
  0.16 * (1 - models$decision_influence) +
  0.14 * (1 - models$accountability) +
  0.14 * (1 - models$community_authority) +
  0.12 * (1 - models$justice_safeguards) +
  0.10 * (1 - models$representation) +
  0.08 * (1 - models$deliberative_quality) +
  0.08 * (1 - models$inclusion),
  4
)

models <- models[order(-models$democratic_futures_capacity_score), ]

representation$representation_quality_score <- round(
  0.20 * representation$affectedness +
  0.20 * representation$representation_quality +
  0.16 * representation$barrier_reduction +
  0.12 * representation$compensation +
  0.14 * representation$decision_access +
  0.08 * representation$trust_condition +
  0.10 * representation$knowledge_recognition,
  4
)

representation <- representation[order(-representation$representation_quality_score), ]

uptake$decision_uptake_score <- round(
  0.18 * uptake$response_duty +
  0.16 * uptake$budget_connection +
  0.16 * uptake$policy_influence +
  0.14 * uptake$regulatory_influence +
  0.14 * uptake$implementation_tracking +
  0.12 * uptake$public_reporting +
  0.10 * uptake$remedy_access,
  4
)

uptake <- uptake[order(-uptake$decision_uptake_score), ]

write.csv(models, file.path(outputs_dir, "r_participation_model_scores.csv"), row.names = FALSE)
write.csv(representation, file.path(outputs_dir, "r_representation_quality_scores.csv"), row.names = FALSE)
write.csv(uptake, file.path(outputs_dir, "r_decision_uptake_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_democratic_futures_capacity_scores.png"), width = 1200, height = 800)
barplot(
  models$democratic_futures_capacity_score,
  names.arg = models$participation_model,
  horiz = TRUE,
  las = 1,
  main = "Democratic Futures Capacity by Participation Model",
  xlab = "Capacity score"
)
dev.off()

png(file.path(outputs_dir, "r_tokenism_risk_scores.png"), width = 1200, height = 800)
barplot(
  models$tokenism_risk_score,
  names.arg = models$participation_model,
  horiz = TRUE,
  las = 1,
  main = "Tokenism Risk by Participation Model",
  xlab = "Tokenism risk"
)
dev.off()

print(models[, c("model_id", "participation_model", "democratic_futures_capacity_score", "tokenism_risk_score")])
print(uptake[, c("uptake_id", "decision_area", "decision_uptake_score", "budget_connection", "remedy_access")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
