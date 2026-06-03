package main

import "fmt"

func regulatoryCapacity(foresight float64, monitoring float64, enforcement float64, rights float64, participation float64, revision float64, learning float64, capture float64, certainty float64, remedy float64) float64 {
	return 0.13*foresight + 0.12*monitoring + 0.12*enforcement + 0.14*rights + 0.10*participation + 0.12*revision + 0.10*learning + 0.08*capture + 0.05*certainty + 0.04*remedy
}

func main() {
	score := regulatoryCapacity(0.70, 0.76, 0.78, 0.90, 0.62, 0.72, 0.74, 0.72, 0.66, 0.86)
	fmt.Printf("Rights-Centered Technology Regulation capacity=%.4f\n", score)
}
