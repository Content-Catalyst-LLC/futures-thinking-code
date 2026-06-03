package main

import "fmt"

func consequencePriority(v []float64) float64 {
	return 0.22*v[0] + 0.26*v[1] + 0.14*v[2] + 0.22*v[3] + 0.16*v[4]
}

func main() {
	heatHealth := []float64{0.84, 0.90, 0.36, 0.94, 0.78}
	fmt.Printf("Heat-related health emergencies consequence priority=%.4f\n", consequencePriority(heatHealth))
}
