#include <iostream>
#include <vector>

double structural_pressure(const std::vector<double>& v) {
    return 0.26 * v[0] + 0.22 * (1.0 - v[1]) + 0.18 * (1.0 - v[2]) + 0.18 * v[3] + 0.16 * v[4];
}

int main() {
    std::vector<double> climate_adaptation = {0.86, 0.46, 0.52, 0.88, 0.90};
    std::cout << "Climate adaptation structural pressure="
              << structural_pressure(climate_adaptation) << "\n";
    return 0;
}
