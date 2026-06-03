package main
import "fmt"
func dataQuality(c float64, v float64, f float64, t float64) float64 { return 0.25*c + 0.25*v + 0.25*f + 0.25*t }
func main() { fmt.Printf("Public trust driver data quality=%.4f\n", dataQuality(1.0,0.95,0.78,0.70)) }
