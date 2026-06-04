package main

import "fmt"

func foresightCapability(signal float64, scenario float64, learning float64, governance float64, adaptive float64, participation float64, ethics float64, data float64) float64 {
	return 0.16*signal + 0.16*scenario + 0.14*learning + 0.14*governance + 0.12*adaptive + 0.10*participation + 0.10*ethics + 0.08*data
}

func main() {
	score := foresightCapability(0.76, 0.74, 0.72, 0.70, 0.66, 0.66, 0.72, 0.68)
	fmt.Printf("Climate Adaptation Authority foresight_capability=%.4f\n", score)
}
