package main

import "fmt"

func boundaryPressure(climate float64, biosphere float64, land float64, freshwater float64, nutrient float64, ocean float64, aerosol float64, novel float64, technology float64) float64 {
	return 0.16*climate + 0.16*biosphere + 0.12*land + 0.12*freshwater + 0.10*nutrient + 0.10*ocean + 0.08*aerosol + 0.10*novel + 0.06*technology
}

func safeJustScore(social float64, governance float64, justice float64, regeneration float64, pressure float64, technology float64) float64 {
	return 0.22*social + 0.20*governance + 0.20*justice + 0.14*regeneration - 0.20*pressure + 0.04*(1-technology)
}

func main() {
	pressure := boundaryPressure(0.32, 0.30, 0.34, 0.30, 0.32, 0.34, 0.30, 0.36, 0.56)
	score := safeJustScore(0.82, 0.80, 0.84, 0.78, pressure, 0.56)
	fmt.Printf("Safe and Just Transformation boundary_pressure=%.4f safe_and_just_score=%.4f\n", pressure, score)
}
