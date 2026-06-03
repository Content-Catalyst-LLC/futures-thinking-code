package main

import "fmt"

func developmentQuality(growth float64, inequality float64, ecology float64, institutions float64, resilience float64, fiscal float64, labor float64, publicInvestment float64, tech float64, trade float64, legitimacy float64) float64 {
	return 0.14*growth - 0.12*inequality - 0.14*ecology + 0.13*institutions + 0.12*resilience + 0.08*fiscal + 0.08*labor + 0.08*publicInvestment + 0.06*tech + 0.03*trade + 0.02*legitimacy
}

func main() {
	score := developmentQuality(0.64, 0.42, 0.36, 0.76, 0.79, 0.68, 0.70, 0.78, 0.68, 0.72, 0.70)
	fmt.Printf("Green Coordinated Transition development_quality=%.4f\n", score)
}
