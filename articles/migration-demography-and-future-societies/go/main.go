package main

import "fmt"

func demographicStress(aging float64, youth float64, migration float64, care float64, housing float64, labor float64, climate float64, cohesion float64, gender float64, health float64) float64 {
	return 0.13*aging + 0.13*youth + 0.12*migration + 0.13*(1-care) + 0.12*housing + 0.10*(1-labor) + 0.11*climate + 0.08*(1-cohesion) + 0.05*(1-gender) + 0.03*(1-health)
}

func main() {
	score := demographicStress(0.62, 0.70, 0.80, 0.34, 0.74, 0.36, 0.62, 0.22, 0.28, 0.38)
	fmt.Printf("Demographic Fear Politics stress=%.4f\n", score)
}
