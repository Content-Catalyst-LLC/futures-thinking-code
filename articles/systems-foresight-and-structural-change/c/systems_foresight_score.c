#include <stdio.h>

double structural_pressure(double v[]) {
    return 0.26 * v[0] + 0.22 * (1.0 - v[1]) + 0.18 * (1.0 - v[2]) + 0.18 * v[3] + 0.16 * v[4];
}

int main(void) {
    double climate_adaptation[] = {0.86, 0.46, 0.52, 0.88, 0.90};
    printf("Climate adaptation structural pressure: %.4f\n", structural_pressure(climate_adaptation));
    return 0;
}
