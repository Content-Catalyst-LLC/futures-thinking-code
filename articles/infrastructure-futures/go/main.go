package main

import "fmt"

func infrastructureViability(centralization float64, redundancy float64, digital float64, climate float64, coordination float64, finance float64, maintenance float64, equity float64, geopolitics float64) float64 {
	return 0.14*(1-centralization) + 0.18*redundancy - 0.12*digital - 0.16*climate + 0.16*coordination + 0.12*finance + 0.12*maintenance + 0.10*equity - 0.08*geopolitics
}

func main() {
	score := infrastructureViability(0.46, 0.78, 0.58, 0.42, 0.78, 0.76, 0.80, 0.76, 0.38)
	fmt.Printf("Adaptive Public Infrastructure viability=%.4f\n", score)
}
