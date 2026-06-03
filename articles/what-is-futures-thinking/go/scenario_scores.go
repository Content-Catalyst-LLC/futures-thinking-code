package main

import "fmt"

func mean(values []float64) float64 {
	total := 0.0
	for _, value := range values {
		total += value
	}
	return total / float64(len(values))
}

func min(values []float64) float64 {
	result := values[0]
	for _, value := range values {
		if value < result {
			result = value
		}
	}
	return result
}

func max(values []float64) float64 {
	result := values[0]
	for _, value := range values {
		if value > result {
			result = value
		}
	}
	return result
}

func robustnessScore(values []float64) float64 {
	meanValue := mean(values)
	worst := min(values)
	rangeValue := max(values) - min(values)

	return 0.50*worst + 0.30*meanValue - 0.20*rangeValue
}

func main() {
	values := []float64{0.72, 0.78, 0.74, 0.73, 0.69, 0.80}

	fmt.Println("Scenario robustness score:")
	fmt.Printf("%.3f\n", robustnessScore(values))
}
