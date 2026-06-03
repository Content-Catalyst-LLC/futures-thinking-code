#include <stdio.h>

double just_capacity(double institution, double equity, double legitimacy, double cohesion, double ecology, double economy) {
    return 0.22 * institution + 0.22 * equity + 0.20 * legitimacy
        + 0.18 * cohesion + 0.10 * (1.0 - ecology) + 0.08 * economy;
}

int main(void) {
    printf("Justice-centered public transformation capacity: %.4f\n",
           just_capacity(0.78, 0.86, 0.82, 0.74, 0.44, 0.68));
    return 0;
}
