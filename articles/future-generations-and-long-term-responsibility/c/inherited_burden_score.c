#include <stdio.h>

double inherited_burden(double climate, double debt, double infrastructure, double ecology, double institution, double tech_lock, double adaptive, double representation) {
    return 0.18 * climate + 0.14 * debt + 0.16 * infrastructure + 0.18 * ecology + 0.14 * tech_lock
        + 0.10 * (1.0 - institution) + 0.06 * (1.0 - adaptive) + 0.04 * (1.0 - representation);
}

int main(void) {
    printf("Short-Term Extraction inherited_burden: %.4f\n",
           inherited_burden(0.88, 0.76, 0.70, 0.84, 0.38, 0.62, 0.36, 0.24));
    return 0;
}
