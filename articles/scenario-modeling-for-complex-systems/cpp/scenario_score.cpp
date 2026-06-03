#include <iostream>
#include <vector>

double viability(const std::vector<double>& v) {
    return 0.35 * v[0] + 0.30 * v[1] + 0.20 * v[2] + 0.15 * v[3];
}

int main() {
    std::vector<double> robust_resilience = {1.55, 1.02, 1.28, 0.15};
    std::cout << "Robust resilience portfolio viability="
              << viability(robust_resilience) << "\n";
    return 0;
}
