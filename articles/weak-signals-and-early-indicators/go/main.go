package main

import "fmt"

func weakSignalProfile(v []float64) float64 {
	return 0.10*v[0] - 0.08*v[1] + 0.24*v[2] + 0.22*v[3] + 0.12*v[4] + 0.12*v[5] + 0.20*v[6]
}

func main() {
	climateInsurance := []float64{0.48, 0.57, 0.90, 0.82, 0.55, 0.86, 0.88}
	fmt.Printf("Climate insurance withdrawal weak signal profile=%.4f\n", weakSignalProfile(climateInsurance))
}
