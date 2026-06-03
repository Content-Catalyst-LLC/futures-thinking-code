#include <stdio.h>

double worst_case_viability(double values[], int n) {
    double worst = values[0];
    for (int i = 1; i < n; i++) {
        if (values[i] < worst) {
            worst = values[i];
        }
    }
    return worst;
}

int main(void) {
    double robust_resilience[] = {0.66, 0.72, 0.78, 0.70};
    printf("Robust resilience portfolio worst-case viability: %.4f\n",
           worst_case_viability(robust_resilience, 4));
    return 0;
}
