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
	values := []float64{0.82, 0.84, 0.88, 0.90, 0.72, 0.84, 0.80}
	weights := []float64{0.15, 0.15, 0.17, 0.13, 0.17, 0.13, 0.10}
	fmt.Printf("Futures-Literate Organization anticipatory capacity=%.4f\n", weightedScore(values, weights))
}
