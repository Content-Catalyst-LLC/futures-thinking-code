package main

import "fmt"

func policyFuturesProfile(robustness float64, equity float64, adaptability float64, coordination float64, legitimacy float64, implementation float64, learning float64, intergenerational float64) float64 {
	return 0.20*robustness + 0.16*equity + 0.18*adaptability + 0.14*coordination + 0.14*legitimacy + 0.08*implementation + 0.06*learning + 0.04*intergenerational
}

func main() {
	score := policyFuturesProfile(0.80, 0.84, 0.82, 0.76, 0.86, 0.56, 0.82, 0.84)
	fmt.Printf("Participatory Anticipatory Policy futures profile=%.4f\n", score)
}
