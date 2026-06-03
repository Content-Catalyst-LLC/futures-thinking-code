package main

import "fmt"

func consumerFutureHealth(affordability float64, trust float64, digital float64, sustainability float64, access float64, price float64, friction float64, regulation float64, privacy float64, local float64) float64 {
	return 0.14*affordability + 0.16*trust + 0.10*sustainability + 0.16*access + 0.10*(1-price) + 0.12*(1-friction) + 0.06*digital + 0.06*regulation + 0.06*privacy + 0.04*local
}

func main() {
	score := consumerFutureHealth(0.70, 0.76, 0.66, 0.70, 0.86, 0.70, 0.42, 0.68, 0.70, 0.76)
	fmt.Printf("Access and Inclusion Market health=%.4f\n", score)
}
