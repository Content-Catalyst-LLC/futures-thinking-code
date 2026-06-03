package main

import (
	"fmt"
	"math"
)

func robustness(values []float64, adaptability float64, equity float64, difficulty float64) float64 {
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

	return 0.45*worst + 0.30*mean + 0.15*adaptability + 0.10*equity - 0.15*volatility - 0.05*difficulty
}

func main() {
	values := []float64{0.78, 0.76, 0.74, 0.71, 0.79}
	fmt.Printf("Flexible Foresight Strategy robustness=%.4f\n", robustness(values, 0.84, 0.72, 0.58))
}
