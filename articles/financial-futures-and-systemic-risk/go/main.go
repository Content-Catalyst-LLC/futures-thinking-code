package main

import "fmt"

func financialResilience(leverage float64, liquidity float64, household float64, climate float64, nonbank float64, digital float64, regulation float64, publicFinance float64, consumer float64, productive float64) float64 {
	return 0.14*liquidity + 0.14*household + 0.14*regulation + 0.10*publicFinance + 0.10*consumer + 0.10*productive + 0.10*(1-leverage) + 0.08*(1-climate) + 0.06*(1-nonbank) + 0.04*(1-digital)
}

func main() {
	score := financialResilience(0.42, 0.82, 0.80, 0.44, 0.48, 0.38, 0.86, 0.78, 0.84, 0.76)
	fmt.Printf("Resilient Public-Interest Finance resilience=%.4f\n", score)
}
