#include <math.h>
#include <stdio.h>

double robustness(double values[], int n, double adaptability, double equity, double difficulty) {
    double sum = 0.0;
    double worst = values[0];

    for (int i = 0; i < n; i++) {
        sum += values[i];
        if (values[i] < worst) {
            worst = values[i];
        }
    }

    double mean = sum / n;
    double variance = 0.0;

    for (int i = 0; i < n; i++) {
        variance += pow(values[i] - mean, 2);
    }

    double volatility = sqrt(variance / n);
    return 0.45 * worst + 0.30 * mean + 0.15 * adaptability + 0.10 * equity - 0.15 * volatility - 0.05 * difficulty;
}

int main(void) {
    double values[] = {0.78, 0.76, 0.74, 0.71, 0.79};
    int n = sizeof(values) / sizeof(values[0]);

    printf("Flexible Foresight Strategy robustness: %.4f\n", robustness(values, n, 0.84, 0.72, 0.58));
    return 0;
}
