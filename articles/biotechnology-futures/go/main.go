package main

import "fmt"

func responsibleCapacity(science float64, governance float64, legitimacy float64, equity float64, manufacturing float64, consent float64, ecologyUncertainty float64, dualUseRisk float64) float64 {
	return 0.16*science + 0.18*governance + 0.16*legitimacy + 0.16*equity + 0.12*manufacturing + 0.12*consent + 0.05*(1-ecologyUncertainty) + 0.05*(1-dualUseRisk)
}

func main() {
	score := responsibleCapacity(0.68, 0.82, 0.84, 0.86, 0.62, 0.88, 0.46, 0.34)
	fmt.Printf("Democratic Biofutures responsible biotechnology capacity=%.4f\n", score)
}
