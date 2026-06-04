package main

import "fmt"

func urbanViability(infrastructure float64, governance float64, housing float64, climate float64, inequality float64, digital float64, finance float64, cohesion float64, maintenance float64) float64 {
	return 0.17*infrastructure + 0.16*governance + 0.14*housing - 0.14*climate - 0.14*inequality + 0.09*digital + 0.12*finance + 0.14*cohesion - 0.08*maintenance
}

func main() {
	score := urbanViability(0.78, 0.78, 0.74, 0.42, 0.40, 0.68, 0.76, 0.74, 0.34)
	fmt.Printf("Adaptive Public City viability=%.4f\n", score)
}
