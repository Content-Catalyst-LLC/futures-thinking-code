package main

import "fmt"

func futuresReadiness(innovation float64, exposure float64, resilience float64, flexibility float64, alignment float64, sensing float64, capital float64, legitimacy float64, transition float64) float64 {
	return 0.14*innovation - 0.10*exposure + 0.15*resilience + 0.14*flexibility + 0.10*alignment + 0.12*sensing + 0.08*capital + 0.09*legitimacy + 0.08*transition
}

func main() {
	score := futuresReadiness(0.82, 0.52, 0.72, 0.79, 0.68, 0.80, 0.66, 0.70, 0.76)
	fmt.Printf("Adaptive Innovation Strategy readiness=%.4f\n", score)
}
