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
	strategies := map[string][]float64{
		"Forecast-Optimized Strategy":   {0.91, 0.42, 0.38, 0.36, 0.40, 0.34},
		"Flexible Foresight Strategy":   {0.78, 0.75, 0.72, 0.70, 0.73, 0.69},
		"Transformational Strategy":     {0.62, 0.81, 0.84, 0.76, 0.78, 0.74},
		"Defensive Continuity Strategy": {0.70, 0.52, 0.55, 0.58, 0.57, 0.60},
	}

	fmt.Println("Futures diagnostics")
	for name, values := range strategies {
		fmt.Printf("%s: robustness=%.4f\n", name, robustness(values))
	}
}
