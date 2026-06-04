package main

import "fmt"

func colonialityRisk(agenda float64, consent float64, land float64, external float64, epistemic float64, benefit float64, harm float64, repair float64, sovereignty float64, data float64, labor float64) float64 {
	return 0.12*agenda + 0.12*(1-consent) + 0.12*land + 0.12*external + 0.11*(1-epistemic) + 0.10*(1-benefit) + 0.10*harm + 0.09*(1-repair) + 0.07*(1-sovereignty) + 0.03*(1-data) + 0.02*(1-labor)
}

func main() {
	score := colonialityRisk(0.86, 0.34, 0.90, 0.82, 0.36, 0.38, 0.78, 0.24, 0.30, 0.28, 0.44)
	fmt.Printf("Green Extraction Continuity coloniality_risk=%.4f\n", score)
}
