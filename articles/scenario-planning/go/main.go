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
	return 0.55*worst + 0.35*mean - 0.10*volatility
}

func main() {
	values := []float64{0.74, 0.76, 0.73, 0.70, 0.80}
	fmt.Printf("Robust Adaptive Strategy robustness=%.4f\n", robustness(values))
}
