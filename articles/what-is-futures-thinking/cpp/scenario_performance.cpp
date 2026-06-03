#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>

double robustness(const std::vector<double>& values, double adaptability, double equity, double difficulty) {
    double mean = std::accumulate(values.begin(), values.end(), 0.0) / values.size();
    double worst = *std::min_element(values.begin(), values.end());
    double variance = 0.0;
    for (double v : values) {
        variance += std::pow(v - mean, 2);
    }
    double volatility = std::sqrt(variance / values.size());
    return 0.45 * worst + 0.30 * mean + 0.15 * adaptability + 0.10 * equity - 0.15 * volatility - 0.05 * difficulty;
}

int main() {
    std::vector<double> flexible = {0.78, 0.76, 0.74, 0.71, 0.79};
    std::cout << "Flexible Foresight Strategy robustness=" << robustness(flexible, 0.84, 0.72, 0.58) << "\n";
    return 0;
}
