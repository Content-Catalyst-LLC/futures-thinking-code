package main
import "fmt"
func enablingScore(m,c,s,i,g,l,e float64) float64 { return 0.16*m + 0.18*c + 0.16*s + 0.16*i + 0.14*g + 0.12*l + 0.08*(1-e) }
func main() { fmt.Printf("Renewable energy acceleration enabling score=%.4f\n", enablingScore(0.78,0.74,0.74,0.68,0.66,0.72,0.48)) }
