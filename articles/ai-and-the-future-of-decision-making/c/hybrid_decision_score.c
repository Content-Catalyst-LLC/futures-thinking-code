#include <stdio.h>

double decision_profile(double human, double machine, double coordination, double transparency, double uncertainty, double accountability, double contestability, double equity) {
    return 0.16 * human + 0.16 * machine + 0.16 * coordination + 0.12 * transparency
        + 0.12 * uncertainty + 0.12 * accountability + 0.08 * contestability + 0.08 * equity;
}

int main(void) {
    printf("High-governance hybrid decision profile: %.4f\n",
           decision_profile(0.72, 0.74, 0.83, 0.79, 0.78, 0.82, 0.80, 0.76));
    return 0;
}
