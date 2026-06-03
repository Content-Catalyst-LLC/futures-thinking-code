package main

import "fmt"

func warningScore(v []float64) float64 {
	return 0.12*v[0] + 0.22*v[1] + 0.20*v[2] + 0.13*v[3] +
		0.11*v[4] + 0.13*v[5] + 0.09*v[6]
}

func main() {
	heatHealth := []float64{0.58, 0.90, 0.88, 0.82, 0.68, 0.92, 0.80}
	fmt.Printf("Rising heat-health emergency demand warning score=%.4f\n", warningScore(heatHealth))
}
