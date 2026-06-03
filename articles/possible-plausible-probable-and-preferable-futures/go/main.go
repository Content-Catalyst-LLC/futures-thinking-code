package main

import "fmt"

func futureScores(v []float64) (float64, float64, float64, float64) {
	plausibility := 0.40*v[0] + 0.35*v[1] + 0.25*v[2]
	probability := 0.70*v[3] + 0.30*v[0]
	preference := 0.30*v[4] + 0.25*v[5] + 0.25*v[6] + 0.20*v[7]
	priority := 0.35*plausibility + 0.25*probability + 0.40*preference
	return plausibility, probability, preference, priority
}

func main() {
	values := []float64{0.62, 0.70, 0.56, 0.42, 0.86, 0.78, 0.84, 0.90}
	plausibility, probability, preference, priority := futureScores(values)
	fmt.Printf("Participatory Anticipatory Governance: plausibility=%.4f probability=%.4f preference=%.4f priority=%.4f\n", plausibility, probability, preference, priority)
}
