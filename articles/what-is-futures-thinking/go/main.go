package main

import (
	"fmt"
	"math"
)

func robustness(values []float64) float64 {
	sum := 0.0
	worst := values[0]
	for _, v := range values {
		sum += v
		if v < worst {
			worst = v
		}
	}
	mean := sum / float64(len(values))
	var variance float64
	for _, v := range values {
		variance += math.Pow(v-mean, 2)
	}
	volatility := math.Sqrt(variance / float64(len(values)))
	return 0.45*worst + 0.35*mean - 0.20*volatility
}

func main() {
	fmt.Printf("Flexible Foresight Strategy robustness=%.4f\n", robustness([]float64{0.78, 0.75, 0.72, 0.70, 0.73, 0.69}))
}
