package main

import "fmt"

func healthResilience(prevention float64, access float64, publicHealth float64, climate float64, workforce float64, tech float64, social float64, trust float64, equity float64, care float64) float64 {
	return 0.13*prevention + 0.12*access + 0.15*publicHealth + 0.10*climate + 0.11*workforce + 0.08*tech + 0.11*social + 0.08*trust + 0.07*equity + 0.05*care
}

func main() {
	score := healthResilience(0.86, 0.84, 0.88, 0.78, 0.76, 0.78, 0.84, 0.82, 0.88, 0.80)
	fmt.Printf("Equitable Health Systems Transformation resilience=%.4f\n", score)
}
