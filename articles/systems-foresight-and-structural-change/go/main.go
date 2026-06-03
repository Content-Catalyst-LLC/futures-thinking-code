package main

import "fmt"

func structuralPressure(v []float64) float64 {
	return 0.26*v[0] + 0.22*(1-v[1]) + 0.18*(1-v[2]) + 0.18*v[3] + 0.16*v[4]
}

func main() {
	climateAdaptation := []float64{0.86, 0.46, 0.52, 0.88, 0.90}
	fmt.Printf("Climate adaptation structural pressure=%.4f\n", structuralPressure(climateAdaptation))
}
