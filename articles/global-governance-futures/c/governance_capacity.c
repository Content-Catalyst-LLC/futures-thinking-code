#include <stdio.h>

double governance_capacity(double institutional, double legitimacy, double law, double finance, double collective, double tech, double planetary, double adaptive, double accountability, double representation) {
    return 0.14 * institutional + 0.16 * legitimacy + 0.12 * law + 0.11 * finance + 0.13 * collective
        + 0.10 * tech + 0.10 * planetary + 0.08 * adaptive + 0.08 * accountability + 0.08 * representation;
}

int main(void) {
    printf("Democratic Justice Governance capacity: %.4f\n",
           governance_capacity(0.82, 0.88, 0.78, 0.80, 0.84, 0.78, 0.86, 0.88, 0.90, 0.92));
    return 0;
}
