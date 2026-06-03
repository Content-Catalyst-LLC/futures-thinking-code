#include <stdio.h>

double adaptive_profile(double learning, double flexibility, double coordination, double legitimacy, double feedback, double resources, double shock, double rigidity, double intergenerational) {
    return 0.18 * learning + 0.16 * flexibility + 0.16 * coordination + 0.14 * legitimacy
        + 0.14 * feedback + 0.10 * resources + 0.08 * shock - 0.10 * rigidity + 0.04 * intergenerational;
}

int main(void) {
    printf("Participatory Governance Assembly adaptive profile: %.4f\n",
           adaptive_profile(0.72, 0.68, 0.66, 0.86, 0.76, 0.54, 0.70, 0.40, 0.82));
    return 0;
}
