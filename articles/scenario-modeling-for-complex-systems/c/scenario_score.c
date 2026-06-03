#include <stdio.h>

double viability(double v[]) {
    return 0.35 * v[0] + 0.30 * v[1] + 0.20 * v[2] + 0.15 * v[3];
}

int main(void) {
    double robust_resilience[] = {1.55, 1.02, 1.28, 0.15};
    printf("Robust resilience portfolio viability: %.4f\n", viability(robust_resilience));
    return 0;
}
