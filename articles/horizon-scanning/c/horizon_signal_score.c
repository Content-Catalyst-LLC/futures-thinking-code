#include <stdio.h>

double horizon_profile(double v[]) {
    return 0.10 * v[0] - 0.08 * v[1] + 0.22 * v[2] + 0.18 * v[3] + 0.14 * v[4] + 0.14 * v[5] + 0.30 * v[6];
}

int main(void) {
    double climate_insurance[] = {0.48, 0.57, 0.90, 0.82, 0.72, 0.84, 0.91};
    printf("Climate insurance withdrawal signal profile: %.4f\n", horizon_profile(climate_insurance));
    return 0;
}
