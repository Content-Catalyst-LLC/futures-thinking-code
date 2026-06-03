args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("--file=", args, value = TRUE)
if (length(file_arg) > 0) { script_path <- normalizePath(sub("--file=", "", file_arg)); root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE) } else { root <- normalizePath(".", mustWork = TRUE) }
data_dir <- file.path(root, "data"); outputs_dir <- file.path(root, "outputs"); dir.create(outputs_dir, showWarnings = FALSE, recursive = TRUE)
drivers <- read.csv(file.path(data_dir, "drivers.csv")); scenarios <- read.csv(file.path(data_dir, "scenarios.csv")); assumptions <- read.csv(file.path(data_dir, "assumptions.csv"))
drivers$data_quality_score <- round(0.25*drivers$completeness + 0.25*drivers$validity + 0.25*drivers$freshness + 0.25*drivers$source_traceability, 4)
drivers$driver_priority_score <- round(drivers$impact * drivers$uncertainty, 4)
drivers <- drivers[order(-drivers$data_quality_score, -drivers$driver_priority_score), ]
scenarios$linked_driver_count <- sapply(strsplit(as.character(scenarios$linked_drivers), ";"), length)
scenarios$review_status_score <- ifelse(scenarios$review_status == "reviewed", 1.0, 0.65)
scenarios$scenario_traceability_score <- round(0.35*pmin(scenarios$linked_driver_count/5,1) + 0.30*pmin(scenarios$assumption_count/6,1) + 0.25*pmin(scenarios$evidence_note_count/10,1) + 0.10*scenarios$review_status_score, 4)
scenarios$traceability_class <- ifelse(scenarios$scenario_traceability_score >= 0.80, "Strong traceability", ifelse(scenarios$scenario_traceability_score >= 0.65, "Moderate traceability", "Weak traceability"))
scenarios <- scenarios[order(-scenarios$scenario_traceability_score), ]
assumptions$assumption_fragility_score <- round(0.35*(1-assumptions$confidence) + 0.35*assumptions$fragility + 0.30*assumptions$strategic_impact, 4)
assumptions <- assumptions[order(-assumptions$assumption_fragility_score), ]
write.csv(drivers, file.path(outputs_dir, "r_driver_data_quality_scores.csv"), row.names = FALSE); write.csv(scenarios, file.path(outputs_dir, "r_scenario_traceability_scores.csv"), row.names = FALSE); write.csv(assumptions, file.path(outputs_dir, "r_assumption_fragility_scores.csv"), row.names = FALSE)
png(file.path(outputs_dir, "r_driver_data_quality_scores.png"), width=1200, height=800); barplot(drivers$data_quality_score, names.arg=drivers$driver_name, horiz=TRUE, las=1, main="Driver Data Quality Scores", xlab="Data quality score"); dev.off()
png(file.path(outputs_dir, "r_scenario_traceability_scores.png"), width=1200, height=800); barplot(scenarios$scenario_traceability_score, names.arg=scenarios$scenario_name, horiz=TRUE, las=1, main="Scenario Traceability Scores", xlab="Traceability score"); dev.off()
print(drivers[, c("driver_id", "driver_name", "data_quality_score", "driver_priority_score")]); print(scenarios[, c("scenario_id", "scenario_name", "scenario_traceability_score", "traceability_class")]); cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
