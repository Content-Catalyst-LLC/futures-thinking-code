package main

import "fmt"

func climateReadiness(emissions float64, adaptation float64, ecosystem float64, governance float64, vulnerability float64, technology float64, transition float64, justice float64, residualLoss float64) float64 {
	return -0.16*emissions + 0.15*adaptation - 0.15*ecosystem + 0.14*governance - 0.12*vulnerability + 0.10*technology + 0.14*transition + 0.12*justice - 0.10*residualLoss
}

func main() {
	score := climateReadiness(0.26, 0.78, 0.34, 0.78, 0.34, 0.70, 0.76, 0.82, 0.28)
	fmt.Printf("Just Climate Transformation readiness=%.4f\n", score)
}
