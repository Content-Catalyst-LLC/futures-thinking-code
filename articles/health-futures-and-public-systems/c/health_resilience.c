#include <stdio.h>

double health_resilience(double prevention, double access, double public_health, double climate, double workforce, double tech, double social, double trust, double equity, double care) {
    return 0.13 * prevention + 0.12 * access + 0.15 * public_health + 0.10 * climate
        + 0.11 * workforce + 0.08 * tech + 0.11 * social + 0.08 * trust
        + 0.07 * equity + 0.05 * care;
}

int main(void) {
    printf("Equitable Health Systems Transformation resilience: %.4f\n",
           health_resilience(0.86, 0.84, 0.88, 0.78, 0.76, 0.78, 0.84, 0.82, 0.88, 0.80));
    return 0;
}
