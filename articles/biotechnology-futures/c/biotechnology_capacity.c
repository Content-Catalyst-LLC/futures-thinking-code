#include <stdio.h>

double responsible_capacity(double science, double governance, double legitimacy, double equity, double manufacturing, double consent, double ecology_uncertainty, double dual_use_risk) {
    return 0.16 * science + 0.18 * governance + 0.16 * legitimacy + 0.16 * equity
        + 0.12 * manufacturing + 0.12 * consent + 0.05 * (1.0 - ecology_uncertainty) + 0.05 * (1.0 - dual_use_risk);
}

int main(void) {
    printf("Democratic Biofutures responsible biotechnology capacity: %.4f\n",
           responsible_capacity(0.68, 0.82, 0.84, 0.86, 0.62, 0.88, 0.46, 0.34));
    return 0;
}
