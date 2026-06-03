#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Biotechnology Futures..."

python3 python/biotechnology_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/biotechnology_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/biotechnology_futures_schema.db
  sqlite3 outputs/biotechnology_futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/biotechnology_capacity.jl > outputs/julia_biotechnology_capacity_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_biotechnology_capacity_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_biotechnology_capacity_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/biotechnology_capacity.cpp -o outputs/biotechnology_capacity_cpp
  ./outputs/biotechnology_capacity_cpp > outputs/cpp_biotechnology_capacity_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/biotechnology_capacity.c -o outputs/biotechnology_capacity_c
  ./outputs/biotechnology_capacity_c > outputs/c_biotechnology_capacity_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/biotechnology_capacity.f90 -o outputs/biotechnology_capacity_fortran
  ./outputs/biotechnology_capacity_fortran > outputs/fortran_biotechnology_capacity_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
