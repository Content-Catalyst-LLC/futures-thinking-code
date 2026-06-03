#include <stdio.h>

double weighted_score(double values[], double weights[], int n) {
    double score = 0.0;
    for (int i = 0; i < n; i++) {
        score += values[i] * weights[i];
    }
    return score;
}

int main(void) {
    double values[] = {0.42, 0.82, 0.84, 0.72, 0.62, 0.76, 0.86};
    double weights[] = {0.16, 0.14, 0.16, 0.18, 0.14, 0.10, 0.12};
    int n = sizeof(values) / sizeof(values[0]);
    printf("Scenario Planning foresight method profile: %.4f\n", weighted_score(values, weights, n));
    return 0;
}
