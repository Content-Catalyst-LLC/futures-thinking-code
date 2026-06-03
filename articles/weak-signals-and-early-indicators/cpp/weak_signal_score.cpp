#include <iostream>
#include <vector>

double weak_signal_profile(const std::vector<double>& v) {
    return 0.10 * v[0] - 0.08 * v[1] + 0.24 * v[2] + 0.22 * v[3] + 0.12 * v[4] + 0.12 * v[5] + 0.20 * v[6];
}

int main() {
    std::vector<double> climate_insurance = {0.48, 0.57, 0.90, 0.82, 0.55, 0.86, 0.88};
    std::cout << "Climate insurance withdrawal weak signal profile="
              << weak_signal_profile(climate_insurance) << "\n";
    return 0;
}
