#include <iostream>
#include <vector>

double weighted_score(const std::vector<double>& values, const std::vector<double>& weights) {
    double score = 0.0;
    for (std::size_t i = 0; i < values.size(); ++i) {
        score += values[i] * weights[i];
    }
    return score;
}

int main() {
    std::vector<double> values = {0.42, 0.82, 0.84, 0.72, 0.62, 0.76, 0.86};
    std::vector<double> weights = {0.16, 0.14, 0.16, 0.18, 0.14, 0.10, 0.12};
    std::cout << "Scenario Planning foresight method profile="
              << weighted_score(values, weights) << "\n";
    return 0;
}
