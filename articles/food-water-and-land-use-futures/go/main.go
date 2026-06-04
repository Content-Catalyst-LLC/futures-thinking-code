package main

import "fmt"

func fwlResilience(production float64, water float64, soil float64, biodiversity float64, governance float64, climate float64, market float64, justice float64, livelihoods float64) float64 {
	return 0.13*production + 0.16*water + 0.15*soil + 0.14*biodiversity + 0.14*governance - 0.12*climate - 0.08*market + 0.14*justice + 0.12*livelihoods
}

func main() {
	score := fwlResilience(0.72, 0.76, 0.82, 0.78, 0.76, 0.42, 0.38, 0.80, 0.78)
	fmt.Printf("Regenerative Transition resilience=%.4f\n", score)
}
