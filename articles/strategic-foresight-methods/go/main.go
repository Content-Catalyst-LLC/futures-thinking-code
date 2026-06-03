package main

import "fmt"

func weightedScore(values []float64, weights []float64) float64 {
	score := 0.0
	for i := range values {
		score += values[i] * weights[i]
	}
	return score
}

func main() {
	values := []float64{0.42, 0.82, 0.84, 0.72, 0.62, 0.76, 0.86}
	weights := []float64{0.16, 0.14, 0.16, 0.18, 0.14, 0.10, 0.12}
	fmt.Printf("Scenario Planning foresight method profile=%.4f\n", weightedScore(values, weights))
}
