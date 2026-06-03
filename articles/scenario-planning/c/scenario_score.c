#include <math.h>
#include <stdio.h>

double robustness(double values[], int n) {
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
    return 0.55 * worst + 0.35 * mean - 0.10 * volatility;
}

int main(void) {
    double values[] = {0.74, 0.76, 0.73, 0.70, 0.80};
    int n = sizeof(values) / sizeof(values[0]);

    printf("Robust Adaptive Strategy robustness: %.4f\n", robustness(values, n));
    return 0;
}
