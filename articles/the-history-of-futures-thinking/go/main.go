package main

import "fmt"

func reflectiveScore(methodological float64, participation float64, ethics float64, systems float64) float64 {
	return 0.25*methodological + 0.25*participation + 0.25*ethics + 0.25*systems
}

func powerRisk(institutionalPower float64, participation float64, ethics float64) float64 {
	return institutionalPower * (1 - participation) * (1 - ethics)
}

func main() {
	score := reflectiveScore(0.68, 0.92, 0.86, 0.64)
	risk := powerRisk(0.42, 0.92, 0.86)
	fmt.Printf("Participatory and Democratic Futures: reflective_score=%.4f power_risk=%.4f\n", score, risk)
}
