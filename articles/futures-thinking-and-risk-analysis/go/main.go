package main

import "fmt"

func futuresRisk(probability float64, structural float64, interdependence float64, vulnerability float64, resilience float64, governance float64, signal float64, tail float64, distributional float64, adaptive float64) float64 {
	return 0.12*(1-probability) + 0.16*structural + 0.14*interdependence + 0.15*vulnerability - 0.11*resilience - 0.10*governance - 0.08*signal + 0.12*tail + 0.10*distributional - 0.02*adaptive
}

func main() {
	score := futuresRisk(0.18, 0.88, 0.91, 0.84, 0.31, 0.28, 0.26, 0.94, 0.92, 0.30)
	fmt.Printf("Systemic Cascade futures_risk_score=%.4f\n", score)
}
