#include <stdio.h>

double weak_signal_profile(double v[]) {
    return 0.10 * v[0] - 0.08 * v[1] + 0.24 * v[2] + 0.22 * v[3] + 0.12 * v[4] + 0.12 * v[5] + 0.20 * v[6];
}

int main(void) {
    double climate_insurance[] = {0.48, 0.57, 0.90, 0.82, 0.55, 0.86, 0.88};
    printf("Climate insurance withdrawal weak signal profile: %.4f\n", weak_signal_profile(climate_insurance));
    return 0;
}
