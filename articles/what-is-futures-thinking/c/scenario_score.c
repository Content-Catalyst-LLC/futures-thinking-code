#include <math.h>
#include <stdio.h>

double robustness(double values[], int n) {
    double sum = 0.0;
    double worst = values[0];
    for (int i = 0; i < n; i++) {
        sum += values[i];
        if (values[i] < worst) worst = values[i];
    }
    double mean = sum / n;
    double variance = 0.0;
    for (int i = 0; i < n; i++) {
        variance += pow(values[i] - mean, 2);
    }
    double volatility = sqrt(variance / n);
    return 0.45 * worst + 0.35 * mean - 0.20 * volatility;
}

int main(void) {
    double values[] = {0.78, 0.75, 0.72, 0.70, 0.73, 0.69};
    int n = sizeof(values) / sizeof(values[0]);
    printf("Flexible Foresight Strategy robustness: %.4f\n", robustness(values, n));
    return 0;
}
