#include <stdio.h>

double ethical_profile(double intergen, double inclusion, double accountability, double risk_equity, double transparency, double contestability, double precaution, double learning, double epistemic, double legitimacy) {
    return 0.13 * intergen + 0.12 * inclusion + 0.12 * accountability + 0.12 * risk_equity
        + 0.10 * transparency + 0.10 * contestability + 0.10 * precaution
        + 0.08 * learning + 0.08 * epistemic + 0.05 * legitimacy;
}

int main(void) {
    printf("Civil Society Coalition ethical_futures_profile: %.4f\n",
           ethical_profile(0.72, 0.84, 0.76, 0.82, 0.78, 0.80, 0.74, 0.72, 0.86, 0.82));
    return 0;
}
