#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Public-Sector Foresight Capacity..."

python3 python/public_sector_foresight_capacity_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/public_sector_foresight_capacity_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/public_sector_foresight_capacity_schema.db
  sqlite3 outputs/public_sector_foresight_capacity_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/foresight_capacity.jl > outputs/julia_foresight_capacity_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_foresight_capacity_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_foresight_capacity_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/foresight_capacity.cpp -o outputs/foresight_capacity_cpp
  ./outputs/foresight_capacity_cpp > outputs/cpp_foresight_capacity_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/foresight_capacity.c -o outputs/foresight_capacity_c
  ./outputs/foresight_capacity_c > outputs/c_foresight_capacity_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/foresight_capacity.f90 -o outputs/foresight_capacity_fortran
  ./outputs/foresight_capacity_fortran > outputs/fortran_foresight_capacity_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
