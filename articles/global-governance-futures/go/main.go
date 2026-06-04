package main

import "fmt"

func governanceCapacity(institutional float64, legitimacy float64, law float64, finance float64, collective float64, tech float64, planetary float64, adaptive float64, accountability float64, representation float64) float64 {
	return 0.14*institutional + 0.16*legitimacy + 0.12*law + 0.11*finance + 0.13*collective + 0.10*tech + 0.10*planetary + 0.08*adaptive + 0.08*accountability + 0.08*representation
}

func main() {
	score := governanceCapacity(0.82, 0.88, 0.78, 0.80, 0.84, 0.78, 0.86, 0.88, 0.90, 0.92)
	fmt.Printf("Democratic Justice Governance capacity=%.4f\n", score)
}
