#include <stdio.h>

int main(void) {
    double values[] = {0.72, 0.78, 0.74, 0.73, 0.69, 0.80};
    int n = 6;

    double total = 0.0;
    double worst = values[0];
    double best = values[0];

    for (int i = 0; i < n; i++) {
        total += values[i];

        if (values[i] < worst) {
            worst = values[i];
        }

        if (values[i] > best) {
            best = values[i];
        }
    }

    double mean = total / n;
    double range = best - worst;
    double score = 0.50 * worst + 0.30 * mean - 0.20 * range;

    printf("Scenario robustness score: %.3f\n", score);

    return 0;
}
