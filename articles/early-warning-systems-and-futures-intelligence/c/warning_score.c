#include <stdio.h>

double warning_score(double v[]) {
    return 0.12 * v[0] + 0.22 * v[1] + 0.20 * v[2] + 0.13 * v[3]
        + 0.11 * v[4] + 0.13 * v[5] + 0.09 * v[6];
}

int main(void) {
    double heat_health[] = {0.58, 0.90, 0.88, 0.82, 0.68, 0.92, 0.80};
    printf("Rising heat-health emergency demand warning score: %.4f\n",
           warning_score(heat_health));
    return 0;
}
