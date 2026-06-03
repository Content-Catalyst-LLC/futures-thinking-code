#include <stdio.h>

double strategic_priority(double v[]) {
    double plausibility = 0.40 * v[0] + 0.35 * v[1] + 0.25 * v[2];
    double probability = 0.70 * v[3] + 0.30 * v[0];
    double preference = 0.30 * v[4] + 0.25 * v[5] + 0.25 * v[6] + 0.20 * v[7];
    return 0.35 * plausibility + 0.25 * probability + 0.40 * preference;
}

int main(void) {
    double values[] = {0.62, 0.70, 0.56, 0.42, 0.86, 0.78, 0.84, 0.90};
    printf("Participatory Anticipatory Governance priority: %.4f\n", strategic_priority(values));
    return 0;
}
