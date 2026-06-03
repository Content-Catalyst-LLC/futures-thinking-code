#include <stdio.h>

double weighted_score(double values[], double weights[], int n) {
    double score = 0.0;
    for (int i = 0; i < n; i++) {
        score += values[i] * weights[i];
    }
    return score;
}

int main(void) {
    double values[] = {0.82, 0.84, 0.88, 0.90, 0.72, 0.84, 0.80};
    double weights[] = {0.15, 0.15, 0.17, 0.13, 0.17, 0.13, 0.10};
    int n = sizeof(values) / sizeof(values[0]);
    printf("Futures-Literate Organization anticipatory capacity: %.4f\n", weighted_score(values, weights, n));
    return 0;
}
