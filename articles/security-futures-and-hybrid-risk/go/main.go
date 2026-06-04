package main

import "fmt"

func hybridRisk(cyber float64, infra float64, info float64, climate float64, resource float64, coordination float64, protection float64, adaptive float64, trust float64, attribution float64) float64 {
	return 0.13*cyber + 0.13*infra + 0.13*info + 0.12*climate + 0.10*resource + 0.11*(1-coordination) + 0.10*(1-protection) + 0.10*(1-adaptive) + 0.05*(1-trust) + 0.03*(1-attribution)
}

func main() {
	score := hybridRisk(0.88, 0.92, 0.90, 0.88, 0.84, 0.22, 0.20, 0.18, 0.16, 0.22)
	fmt.Printf("Systemic Security Breakdown hybrid_risk=%.4f\n", score)
}
