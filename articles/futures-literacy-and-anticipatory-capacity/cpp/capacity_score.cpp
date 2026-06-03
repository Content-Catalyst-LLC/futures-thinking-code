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
    std::vector<double> values = {0.82, 0.84, 0.88, 0.90, 0.72, 0.84, 0.80};
    std::vector<double> weights = {0.15, 0.15, 0.17, 0.13, 0.17, 0.13, 0.10};
    std::cout << "Futures-Literate Organization anticipatory capacity="
              << weighted_score(values, weights) << "\n";
    return 0;
}
