package main

import "fmt"

func justCapacity(institution float64, equity float64, legitimacy float64, cohesion float64, ecology float64, economy float64) float64 {
	return 0.22*institution + 0.22*equity + 0.20*legitimacy + 0.18*cohesion + 0.10*(1-ecology) + 0.08*economy
}

func main() {
	score := justCapacity(0.78, 0.86, 0.82, 0.74, 0.44, 0.68)
	fmt.Printf("Justice-centered public transformation capacity=%.4f\n", score)
}
