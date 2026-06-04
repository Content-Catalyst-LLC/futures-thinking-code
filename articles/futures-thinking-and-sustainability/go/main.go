package main

import "fmt"

func sustainabilityViability(ecology float64, equity float64, adaptive float64, technology float64, governance float64, finance float64, resilience float64, justice float64, degradation float64) float64 {
	return 0.17*ecology + 0.15*equity + 0.14*adaptive + 0.10*technology + 0.14*governance + 0.10*finance + 0.10*resilience + 0.10*justice - 0.08*degradation
}

func main() {
	score := sustainabilityViability(0.82, 0.82, 0.80, 0.70, 0.78, 0.76, 0.82, 0.86, 0.30)
	fmt.Printf("Just Transformative Sustainability viability=%.4f\n", score)
}
