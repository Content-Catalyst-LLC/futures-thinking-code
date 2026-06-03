#include <iostream>
#include <vector>

double pathway_viability(const std::vector<double>& v) {
    return 0.18 * v[0] - 0.16 * v[1] + 0.14 * v[2] + 0.18 * v[3] + 0.16 * v[4] + 0.12 * v[5] + 0.14 * v[6] - 0.12 * v[7];
}

int main() {
    std::vector<double> public_accountability = {0.66, 0.56, 0.52, 0.78, 0.72, 0.86, 0.80, 0.40};
    std::cout << "Public Accountability Before Scale viability="
              << pathway_viability(public_accountability) << "\n";
    return 0;
}
