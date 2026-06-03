package main

import "fmt"

func decisionProfile(human float64, machine float64, coordination float64, transparency float64, uncertainty float64, accountability float64, contestability float64, equity float64) float64 {
	return 0.16*human + 0.16*machine + 0.16*coordination + 0.12*transparency + 0.12*uncertainty + 0.12*accountability + 0.08*contestability + 0.08*equity
}

func main() {
	score := decisionProfile(0.72, 0.74, 0.83, 0.79, 0.78, 0.82, 0.80, 0.76)
	fmt.Printf("High-governance hybrid decision profile=%.4f\n", score)
}
