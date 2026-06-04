#include <stdio.h>

double futures_risk(double probability, double structural, double interdependence, double vulnerability, double resilience, double governance, double signal, double tail, double distributional, double adaptive) {
    return 0.12 * (1.0 - probability) + 0.16 * structural + 0.14 * interdependence + 0.15 * vulnerability
        - 0.11 * resilience - 0.10 * governance - 0.08 * signal + 0.12 * tail
        + 0.10 * distributional - 0.02 * adaptive;
}

int main(void) {
    printf("Systemic Cascade futures_risk_score: %.4f\n",
           futures_risk(0.18, 0.88, 0.91, 0.84, 0.31, 0.28, 0.26, 0.94, 0.92, 0.30));
    return 0;
}
