#include <algorithm>
#include <iostream>
#include <vector>

double worst_case_viability(const std::vector<double>& values) {
    return *std::min_element(values.begin(), values.end());
}

int main() {
    std::vector<double> robust_resilience = {0.66, 0.72, 0.78, 0.70};
    std::cout << "Robust resilience portfolio worst-case viability="
              << worst_case_viability(robust_resilience) << "\n";
    return 0;
}
