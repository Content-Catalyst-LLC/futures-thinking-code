#include <stdio.h>

double democratic_capacity(double inclusion, double deliberation, double representation, double uptake, double accountability, double justice, double learning, double influence, double accessibility, double authority) {
    return 0.11 * inclusion + 0.12 * deliberation + 0.11 * representation + 0.14 * uptake
        + 0.12 * accountability + 0.12 * justice + 0.08 * learning + 0.10 * influence
        + 0.05 * accessibility + 0.05 * authority;
}

int main(void) {
    printf("Co-Governance Futures Board capacity: %.4f\n",
           democratic_capacity(0.82, 0.78, 0.80, 0.78, 0.82, 0.84, 0.78, 0.80, 0.76, 0.86));
    return 0;
}
