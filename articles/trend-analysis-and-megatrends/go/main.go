package main

import "fmt"

func trendProfile(v []float64) float64 {
	return 0.20*v[0] + 0.22*v[1] + 0.22*v[2] - 0.12*v[3] - 0.14*v[4] + 0.10*v[5]
}

func main() {
	climateRisk := []float64{0.74, 0.86, 0.88, 0.22, 0.52, 0.86}
	fmt.Printf("Climate Risk Intensification profile=%.4f\n", trendProfile(climateRisk))
}
