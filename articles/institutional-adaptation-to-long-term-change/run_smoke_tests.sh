#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Institutional Adaptation to Long-Term Change..."

python3 python/institutional_adaptation_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/institutional_adaptation_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/institutional_adaptation_schema.db
  sqlite3 outputs/institutional_adaptation_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/adaptive_profile.jl > outputs/julia_adaptive_profile_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_adaptive_profile_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_adaptive_profile_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/adaptive_profile.cpp -o outputs/adaptive_profile_cpp
  ./outputs/adaptive_profile_cpp > outputs/cpp_adaptive_profile_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/adaptive_profile.c -o outputs/adaptive_profile_c
  ./outputs/adaptive_profile_c > outputs/c_adaptive_profile_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/adaptive_profile.f90 -o outputs/adaptive_profile_fortran
  ./outputs/adaptive_profile_fortran > outputs/fortran_adaptive_profile_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
