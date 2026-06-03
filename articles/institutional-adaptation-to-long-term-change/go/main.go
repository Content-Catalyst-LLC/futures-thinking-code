package main

import "fmt"

func adaptiveProfile(learning float64, flexibility float64, coordination float64, legitimacy float64, feedback float64, resources float64, shock float64, rigidity float64, intergenerational float64) float64 {
	return 0.18*learning + 0.16*flexibility + 0.16*coordination + 0.14*legitimacy + 0.14*feedback + 0.10*resources + 0.08*shock - 0.10*rigidity + 0.04*intergenerational
}

func main() {
	score := adaptiveProfile(0.72, 0.68, 0.66, 0.86, 0.76, 0.54, 0.70, 0.40, 0.82)
	fmt.Printf("Participatory Governance Assembly adaptive profile=%.4f\n", score)
}
