package main

import "fmt"

func jobQuality(wageSecurity float64, workerVoice float64, training float64, protection float64, surveillance float64, initialQuality float64) float64 {
	return 0.28*initialQuality + 0.18*wageSecurity + 0.18*workerVoice + 0.16*protection + 0.12*training + 0.08*(1-surveillance)
}

func main() {
	score := jobQuality(0.66, 0.54, 0.72, 0.60, 0.46, 0.70)
	fmt.Printf("Knowledge work adjusted job quality=%.4f\n", score)
}
