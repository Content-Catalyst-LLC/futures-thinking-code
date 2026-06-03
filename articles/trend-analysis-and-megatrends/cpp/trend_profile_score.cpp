#include <iostream>
#include <vector>

double trend_profile(const std::vector<double>& v) {
    return 0.20 * v[0] + 0.22 * v[1] + 0.22 * v[2] - 0.12 * v[3] - 0.14 * v[4] + 0.10 * v[5];
}

int main() {
    std::vector<double> climate_risk = {0.74, 0.86, 0.88, 0.22, 0.52, 0.86};
    std::cout << "Climate Risk Intensification profile=" << trend_profile(climate_risk) << "\n";
    return 0;
}
