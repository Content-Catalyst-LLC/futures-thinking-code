#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Anticipatory Governance..."

python3 python/anticipatory_governance_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/anticipatory_governance_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/anticipatory_governance_schema.db
  sqlite3 outputs/anticipatory_governance_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/anticipatory_capacity.jl > outputs/julia_anticipatory_capacity_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_anticipatory_capacity_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_anticipatory_capacity_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/anticipatory_capacity.cpp -o outputs/anticipatory_capacity_cpp
  ./outputs/anticipatory_capacity_cpp > outputs/cpp_anticipatory_capacity_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/anticipatory_capacity.c -o outputs/anticipatory_capacity_c
  ./outputs/anticipatory_capacity_c > outputs/c_anticipatory_capacity_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/anticipatory_capacity.f90 -o outputs/anticipatory_capacity_fortran
  ./outputs/anticipatory_capacity_fortran > outputs/fortran_anticipatory_capacity_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
