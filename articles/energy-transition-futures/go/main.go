package main

import "fmt"

func transitionReadiness(clean float64, grid float64, storage float64, electrification float64, phaseDown float64, justice float64, labor float64, materials float64, resilience float64) float64 {
	return 0.14*clean + 0.14*grid + 0.12*storage + 0.12*electrification + 0.12*phaseDown + 0.12*justice + 0.10*labor + 0.08*materials + 0.06*resilience
}

func main() {
	score := transitionReadiness(0.82, 0.78, 0.74, 0.76, 0.78, 0.84, 0.82, 0.76, 0.80)
	fmt.Printf("Managed Just Transition readiness=%.4f\n", score)
}
