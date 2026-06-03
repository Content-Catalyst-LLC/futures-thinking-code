package main

import "fmt"

func publicInterestCapacity(platformPower float64, dataAdvantage float64, interoperability float64, workerProtection float64, publicAccountability float64, userRights float64, ecologicalResponsibility float64, digitalPublicValue float64) float64 {
	return 0.18*interoperability + 0.18*publicAccountability + 0.16*userRights + 0.14*workerProtection + 0.14*digitalPublicValue + 0.10*ecologicalResponsibility + 0.05*(1-platformPower) + 0.05*(1-dataAdvantage)
}

func main() {
	score := publicInterestCapacity(0.42, 0.46, 0.76, 0.70, 0.82, 0.84, 0.70, 0.86)
	fmt.Printf("Digital Public Infrastructure Turn public-interest platform capacity=%.4f\n", score)
}
