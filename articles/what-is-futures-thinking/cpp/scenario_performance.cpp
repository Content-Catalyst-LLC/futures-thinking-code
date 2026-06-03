#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>

double robustness(const std::vector<double>& values) {
    double mean = std::accumulate(values.begin(), values.end(), 0.0) / values.size();
    double worst = *std::min_element(values.begin(), values.end());
    double variance = 0.0;
    for (double v : values) {
        variance += std::pow(v - mean, 2);
    }
    double volatility = std::sqrt(variance / values.size());
    return 0.45 * worst + 0.35 * mean - 0.20 * volatility;
}

int main() {
    std::vector<double> values = {0.78, 0.75, 0.72, 0.70, 0.73, 0.69};
    std::cout << "Flexible Foresight Strategy robustness=" << robustness(values) << "\n";
    return 0;
}
