package main

import "fmt"

func foresightCapacity(scanning float64, scenarios float64, uptake float64, participation float64, budget float64, evaluation float64, learning float64, authority float64, knowledge float64, legitimacy float64) float64 {
	return 0.12*scanning + 0.12*scenarios + 0.14*uptake + 0.12*participation + 0.12*budget + 0.10*evaluation + 0.10*learning + 0.10*authority + 0.05*knowledge + 0.03*legitimacy
}

func main() {
	score := foresightCapacity(0.68, 0.78, 0.68, 0.90, 0.62, 0.76, 0.80, 0.60, 0.72, 0.86)
	fmt.Printf("Participatory Public Foresight System capacity=%.4f\n", score)
}
