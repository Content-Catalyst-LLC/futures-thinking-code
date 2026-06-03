package main

import "fmt"

func viability(v []float64) float64 {
	return 0.35*v[0] + 0.30*v[1] + 0.20*v[2] + 0.15*v[3]
}

func main() {
	robustResilience := []float64{1.55, 1.02, 1.28, 0.15}
	fmt.Printf("Robust resilience portfolio viability=%.4f\n", viability(robustResilience))
}
