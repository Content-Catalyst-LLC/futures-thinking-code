#include <stdio.h>

double resilience_score(double cost, double diversification, double buffer, double visibility, double labor, double climate, double traceability, double circularity, double regulation, double recovery) {
    return 0.10 * cost + 0.16 * diversification + 0.14 * buffer + 0.14 * visibility
        + 0.12 * labor + 0.13 * climate + 0.09 * traceability + 0.06 * circularity
        + 0.04 * regulation + 0.02 * recovery;
}

int main(void) {
    printf("Essential Goods Resilience Model resilience: %.4f\n",
           resilience_score(0.52, 0.76, 0.84, 0.74, 0.72, 0.70, 0.76, 0.54, 0.80, 0.86));
    return 0;
}
