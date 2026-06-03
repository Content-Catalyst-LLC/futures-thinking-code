#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Systems Foresight and Structural Change..."

python3 python/systems_foresight_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/systems_foresight_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/systems_foresight_schema.db
  sqlite3 outputs/systems_foresight_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/systems_foresight_score.jl > outputs/julia_systems_foresight_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_systems_foresight_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_systems_foresight_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/systems_foresight_score.cpp -o outputs/systems_foresight_score_cpp
  ./outputs/systems_foresight_score_cpp > outputs/cpp_systems_foresight_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/systems_foresight_score.c -o outputs/systems_foresight_score_c
  ./outputs/systems_foresight_score_c > outputs/c_systems_foresight_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/systems_foresight_score.f90 -o outputs/systems_foresight_score_fortran
  ./outputs/systems_foresight_score_fortran > outputs/fortran_systems_foresight_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
