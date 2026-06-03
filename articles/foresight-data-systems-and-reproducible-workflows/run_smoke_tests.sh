#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Foresight Data Systems and Reproducible Workflows..."
python3 python/foresight_data_systems_workflow.py
if command -v Rscript >/dev/null 2>&1; then echo "Running R workflow..."; Rscript r/foresight_data_systems_workflow.R; else echo "Skipping R workflow: Rscript not found."; fi
if command -v sqlite3 >/dev/null 2>&1; then echo "Testing SQL schema..."; rm -f outputs/foresight_data_systems_schema.db; sqlite3 outputs/foresight_data_systems_schema.db < sql/schema.sql; else echo "Skipping SQL schema test: sqlite3 not found."; fi
if command -v julia >/dev/null 2>&1; then echo "Running Julia workflow..."; julia julia/data_quality_score.jl > outputs/julia_data_quality_scores.csv; else echo "Skipping Julia workflow: julia not found."; fi
if command -v go >/dev/null 2>&1; then echo "Running Go workflow..."; (cd go && go run main.go) > outputs/go_data_quality_output.txt; else echo "Skipping Go workflow: go not found."; fi
if command -v cargo >/dev/null 2>&1; then echo "Running Rust workflow..."; (cd rust && cargo run --quiet) > outputs/rust_data_quality_output.txt; else echo "Skipping Rust workflow: cargo not found."; fi
if command -v g++ >/dev/null 2>&1; then echo "Running C++ workflow..."; g++ cpp/data_quality_score.cpp -o outputs/data_quality_score_cpp; ./outputs/data_quality_score_cpp > outputs/cpp_data_quality_output.txt; else echo "Skipping C++ workflow: g++ not found."; fi
if command -v gcc >/dev/null 2>&1; then echo "Running C workflow..."; gcc c/data_quality_score.c -o outputs/data_quality_score_c; ./outputs/data_quality_score_c > outputs/c_data_quality_output.txt; else echo "Skipping C workflow: gcc not found."; fi
if command -v gfortran >/dev/null 2>&1; then echo "Running Fortran workflow..."; gfortran fortran/data_quality_score.f90 -o outputs/data_quality_score_fortran; ./outputs/data_quality_score_fortran > outputs/fortran_data_quality_output.txt; else echo "Skipping Fortran workflow: gfortran not found."; fi
echo ""; echo "Smoke tests complete."; echo "Generated outputs:"; find outputs -maxdepth 1 -type f | sort
