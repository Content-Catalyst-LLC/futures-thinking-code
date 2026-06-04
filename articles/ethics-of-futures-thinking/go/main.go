package main

import "fmt"

func ethicalProfile(intergen float64, inclusion float64, accountability float64, riskEquity float64, transparency float64, contestability float64, precaution float64, learning float64, epistemic float64, legitimacy float64) float64 {
	return 0.13*intergen + 0.12*inclusion + 0.12*accountability + 0.12*riskEquity + 0.10*transparency + 0.10*contestability + 0.10*precaution + 0.08*learning + 0.08*epistemic + 0.05*legitimacy
}

func main() {
	score := ethicalProfile(0.72, 0.84, 0.76, 0.82, 0.78, 0.80, 0.74, 0.72, 0.86, 0.82)
	fmt.Printf("Civil Society Coalition ethical_futures_profile=%.4f\n", score)
}
