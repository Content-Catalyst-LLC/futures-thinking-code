package main

import "fmt"

func judgmentProfile(v []float64) float64 {
	return 0.25*v[0] + 0.35*v[1] + 0.25*v[2] + 0.15*v[3]
}

func main() {
	publicAI := []float64{0.69, 0.92, 0.87, 0.61}
	fmt.Printf("Public AI accountability Delphi judgment profile=%.4f\n", judgmentProfile(publicAI))
}
