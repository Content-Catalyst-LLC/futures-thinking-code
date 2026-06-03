package main

import "fmt"

func resilienceScore(cost float64, diversification float64, buffer float64, visibility float64, labor float64, climate float64, traceability float64, circularity float64, regulation float64, recovery float64) float64 {
	return 0.10*cost + 0.16*diversification + 0.14*buffer + 0.14*visibility + 0.12*labor + 0.13*climate + 0.09*traceability + 0.06*circularity + 0.04*regulation + 0.02*recovery
}

func main() {
	score := resilienceScore(0.52, 0.76, 0.84, 0.74, 0.72, 0.70, 0.76, 0.54, 0.80, 0.86)
	fmt.Printf("Essential Goods Resilience Model resilience=%.4f\n", score)
}
