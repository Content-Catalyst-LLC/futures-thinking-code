#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <string>
#include <utility>
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
    std::vector<std::pair<std::string, std::vector<double>>> strategies = {
        {"Forecast-Optimized Strategy", {0.91, 0.42, 0.38, 0.36, 0.40, 0.34}},
        {"Flexible Foresight Strategy", {0.78, 0.75, 0.72, 0.70, 0.73, 0.69}},
        {"Transformational Strategy", {0.62, 0.81, 0.84, 0.76, 0.78, 0.74}},
        {"Defensive Continuity Strategy", {0.70, 0.52, 0.55, 0.58, 0.57, 0.60}}
    };

    std::cout << "Forecasting, foresight, and futures studies diagnostics\n";
    for (const auto& item : strategies) {
        std::cout << item.first << ": robustness=" << robustness(item.second) << "\n";
    }
    return 0;
}
