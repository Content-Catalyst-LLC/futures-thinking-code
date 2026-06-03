#include <iostream>
#include <vector>

double consequence_priority(const std::vector<double>& v) {
    return 0.22 * v[0] + 0.26 * v[1] + 0.14 * v[2] + 0.22 * v[3] + 0.16 * v[4];
}

int main() {
    std::vector<double> heat_health = {0.84, 0.90, 0.36, 0.94, 0.78};
    std::cout << "Heat-related health emergencies consequence priority="
              << consequence_priority(heat_health) << "\n";
    return 0;
}
