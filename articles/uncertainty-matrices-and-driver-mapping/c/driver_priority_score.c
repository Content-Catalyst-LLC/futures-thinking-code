#include <stdio.h>

double driver_priority(double v[]) {
    return 0.22 * v[0] + 0.20 * v[1] + 0.14 * v[2] + 0.14 * v[3]
        + 0.12 * v[4] + 0.08 * v[5] + 0.06 * v[6] + 0.04 * (1.0 - v[7]);
}

int main(void) {
    double public_trust[] = {0.88, 0.82, 0.80, 0.84, 0.84, 0.70, 0.68, 0.54};
    printf("Public trust driver priority: %.4f\n", driver_priority(public_trust));
    return 0;
}
