package main

import "fmt"

func disciplinedHope(hope float64, agency float64, trust float64, institution float64, accountability float64, repair float64, fatigue float64, polarization float64) float64 {
	return 0.18*hope + 0.18*agency + 0.16*trust + 0.16*institution + 0.14*accountability + 0.12*repair - 0.04*fatigue - 0.02*polarization
}

func main() {
	score := disciplinedHope(0.86, 0.84, 0.76, 0.80, 0.88, 0.92, 0.28, 0.30)
	fmt.Printf("Reparative Imagination disciplined_hope=%.4f\n", score)
}
