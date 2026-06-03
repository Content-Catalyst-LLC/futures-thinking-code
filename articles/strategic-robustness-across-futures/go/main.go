package main

import "fmt"

func worstCaseViability(values []float64) float64 {
	worst := values[0]
	for _, value := range values {
		if value < worst {
			worst = value
		}
	}
	return worst
}

func main() {
	robustResilience := []float64{0.66, 0.72, 0.78, 0.70}
	fmt.Printf("Robust resilience portfolio worst-case viability=%.4f\n", worstCaseViability(robustResilience))
}
