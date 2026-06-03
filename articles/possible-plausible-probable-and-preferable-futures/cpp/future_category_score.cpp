#include <iostream>
#include <vector>

struct Scores {
    double plausibility;
    double probability;
    double preference;
    double priority;
};

Scores future_scores(const std::vector<double>& v) {
    double plausibility = 0.40 * v[0] + 0.35 * v[1] + 0.25 * v[2];
    double probability = 0.70 * v[3] + 0.30 * v[0];
    double preference = 0.30 * v[4] + 0.25 * v[5] + 0.25 * v[6] + 0.20 * v[7];
    double priority = 0.35 * plausibility + 0.25 * probability + 0.40 * preference;
    return {plausibility, probability, preference, priority};
}

int main() {
    std::vector<double> values = {0.62, 0.70, 0.56, 0.42, 0.86, 0.78, 0.84, 0.90};
    Scores s = future_scores(values);
    std::cout << "Participatory Anticipatory Governance priority=" << s.priority << "\n";
    return 0;
}
