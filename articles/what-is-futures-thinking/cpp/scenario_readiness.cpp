#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

double robustness_score(const std::vector<double>& values) {
    double mean = std::accumulate(values.begin(), values.end(), 0.0) / values.size();
    double worst = *std::min_element(values.begin(), values.end());
    double best = *std::max_element(values.begin(), values.end());
    double range = best - worst;

    return 0.50 * worst + 0.30 * mean - 0.20 * range;
}

int main() {
    std::vector<double> values = {0.72, 0.78, 0.74, 0.73, 0.69, 0.80};

    std::cout << "Scenario robustness score: " << robustness_score(values) << "\n";

    return 0;
}
