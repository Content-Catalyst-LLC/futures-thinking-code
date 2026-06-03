#include <stdio.h>

double futures_readiness(double innovation, double exposure, double resilience, double flexibility, double alignment, double sensing, double capital, double legitimacy, double transition) {
    return 0.14 * innovation - 0.10 * exposure + 0.15 * resilience + 0.14 * flexibility
        + 0.10 * alignment + 0.12 * sensing + 0.08 * capital + 0.09 * legitimacy + 0.08 * transition;
}

int main(void) {
    printf("Adaptive Innovation Strategy readiness: %.4f\n",
           futures_readiness(0.82, 0.52, 0.72, 0.79, 0.68, 0.80, 0.66, 0.70, 0.76));
    return 0;
}
