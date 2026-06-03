#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for AI and the Future of Decision-Making..."

python3 python/ai_decision_making_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/ai_decision_making_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/ai_decision_making_schema.db
  sqlite3 outputs/ai_decision_making_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/hybrid_decision_score.jl > outputs/julia_hybrid_decision_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_hybrid_decision_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_hybrid_decision_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/hybrid_decision_score.cpp -o outputs/hybrid_decision_score_cpp
  ./outputs/hybrid_decision_score_cpp > outputs/cpp_hybrid_decision_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/hybrid_decision_score.c -o outputs/hybrid_decision_score_c
  ./outputs/hybrid_decision_score_c > outputs/c_hybrid_decision_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/hybrid_decision_score.f90 -o outputs/hybrid_decision_score_fortran
  ./outputs/hybrid_decision_score_fortran > outputs/fortran_hybrid_decision_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
