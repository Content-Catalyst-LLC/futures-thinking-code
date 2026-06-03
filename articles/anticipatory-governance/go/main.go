package main

import "fmt"

func anticipatoryCapacity(detection float64, interpretation float64, scenario float64, preparedness float64, legitimacy float64, coordination float64, adaptive float64, equity float64, learning float64, implementation float64) float64 {
	return 0.12*detection + 0.12*interpretation + 0.12*scenario + 0.12*preparedness + 0.12*legitimacy + 0.10*coordination + 0.10*adaptive + 0.08*equity + 0.07*learning + 0.05*implementation
}

func main() {
	score := anticipatoryCapacity(0.68, 0.74, 0.78, 0.70, 0.86, 0.72, 0.68, 0.88, 0.78, 0.64)
	fmt.Printf("Participatory Anticipatory Governance capacity=%.4f\n", score)
}
