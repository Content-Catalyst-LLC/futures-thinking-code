#include <stdio.h>

double policy_futures_profile(double robustness, double equity, double adaptability, double coordination, double legitimacy, double implementation, double learning, double intergenerational) {
    return 0.20 * robustness + 0.16 * equity + 0.18 * adaptability + 0.14 * coordination
        + 0.14 * legitimacy + 0.08 * implementation + 0.06 * learning + 0.04 * intergenerational;
}

int main(void) {
    printf("Participatory Anticipatory Policy futures profile: %.4f\n",
           policy_futures_profile(0.80, 0.84, 0.82, 0.76, 0.86, 0.56, 0.82, 0.84));
    return 0;
}
