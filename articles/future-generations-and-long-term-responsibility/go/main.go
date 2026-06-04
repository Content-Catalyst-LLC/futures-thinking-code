package main

import "fmt"

func inheritedBurden(climate float64, debt float64, infrastructure float64, ecology float64, institution float64, techLock float64, adaptive float64, representation float64) float64 {
	return 0.18*climate + 0.14*debt + 0.16*infrastructure + 0.18*ecology + 0.14*techLock + 0.10*(1-institution) + 0.06*(1-adaptive) + 0.04*(1-representation)
}

func main() {
	score := inheritedBurden(0.88, 0.76, 0.70, 0.84, 0.38, 0.62, 0.36, 0.24)
	fmt.Printf("Short-Term Extraction inherited_burden=%.4f\n", score)
}
