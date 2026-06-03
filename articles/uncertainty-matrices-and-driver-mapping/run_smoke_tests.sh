#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Uncertainty Matrices and Driver Mapping..."

python3 python/uncertainty_driver_mapping_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/uncertainty_driver_mapping_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/uncertainty_driver_mapping_schema.db
  sqlite3 outputs/uncertainty_driver_mapping_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/driver_priority_score.jl > outputs/julia_driver_priority_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_driver_priority_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_driver_priority_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/driver_priority_score.cpp -o outputs/driver_priority_score_cpp
  ./outputs/driver_priority_score_cpp > outputs/cpp_driver_priority_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/driver_priority_score.c -o outputs/driver_priority_score_c
  ./outputs/driver_priority_score_c > outputs/c_driver_priority_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/driver_priority_score.f90 -o outputs/driver_priority_score_fortran
  ./outputs/driver_priority_score_fortran > outputs/fortran_driver_priority_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
