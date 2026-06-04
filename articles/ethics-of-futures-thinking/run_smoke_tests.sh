#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Ethics of Futures Thinking..."

python3 python/ethics_of_futures_thinking_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/ethics_of_futures_thinking_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/ethics_of_futures_thinking_schema.db
  sqlite3 outputs/ethics_of_futures_thinking_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/ethical_futures_score.jl > outputs/julia_ethical_futures_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_ethical_futures_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_ethical_futures_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/ethical_futures_score.cpp -o outputs/ethical_futures_cpp
  ./outputs/ethical_futures_cpp > outputs/cpp_ethical_futures_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/ethical_futures_score.c -o outputs/ethical_futures_c
  ./outputs/ethical_futures_c > outputs/c_ethical_futures_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/ethical_futures_score.f90 -o outputs/ethical_futures_fortran
  ./outputs/ethical_futures_fortran > outputs/fortran_ethical_futures_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
