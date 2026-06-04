#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Migration, Demography, and Future Societies..."

python3 python/migration_demography_future_societies_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/migration_demography_future_societies_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/migration_demography_future_societies_schema.db
  sqlite3 outputs/migration_demography_future_societies_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/demographic_stress_score.jl > outputs/julia_demographic_stress_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_demographic_stress_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_demographic_stress_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/demographic_stress_score.cpp -o outputs/demographic_stress_cpp
  ./outputs/demographic_stress_cpp > outputs/cpp_demographic_stress_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/demographic_stress_score.c -o outputs/demographic_stress_c
  ./outputs/demographic_stress_c > outputs/c_demographic_stress_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/demographic_stress_score.f90 -o outputs/demographic_stress_fortran
  ./outputs/demographic_stress_fortran > outputs/fortran_demographic_stress_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
