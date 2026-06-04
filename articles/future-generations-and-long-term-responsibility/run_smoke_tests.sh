#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Future Generations and Long-Term Responsibility..."

python3 python/future_generations_long_term_responsibility_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/future_generations_long_term_responsibility_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/future_generations_long_term_responsibility_schema.db
  sqlite3 outputs/future_generations_long_term_responsibility_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/inherited_burden_score.jl > outputs/julia_inherited_burden_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_inherited_burden_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_inherited_burden_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/inherited_burden_score.cpp -o outputs/inherited_burden_cpp
  ./outputs/inherited_burden_cpp > outputs/cpp_inherited_burden_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/inherited_burden_score.c -o outputs/inherited_burden_c
  ./outputs/inherited_burden_c > outputs/c_inherited_burden_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/inherited_burden_score.f90 -o outputs/inherited_burden_fortran
  ./outputs/inherited_burden_fortran > outputs/fortran_inherited_burden_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
