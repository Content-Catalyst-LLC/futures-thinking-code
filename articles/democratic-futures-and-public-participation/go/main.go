package main

import "fmt"

func democraticCapacity(inclusion float64, deliberation float64, representation float64, uptake float64, accountability float64, justice float64, learning float64, influence float64, accessibility float64, authority float64) float64 {
	return 0.11*inclusion + 0.12*deliberation + 0.11*representation + 0.14*uptake + 0.12*accountability + 0.12*justice + 0.08*learning + 0.10*influence + 0.05*accessibility + 0.05*authority
}

func main() {
	score := democraticCapacity(0.82, 0.78, 0.80, 0.78, 0.82, 0.84, 0.78, 0.80, 0.76, 0.86)
	fmt.Printf("Co-Governance Futures Board capacity=%.4f\n", score)
}
