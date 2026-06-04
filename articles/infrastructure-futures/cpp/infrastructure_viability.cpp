#include <iostream>

double infrastructure_viability(double centralization, double redundancy, double digital, double climate, double coordination, double finance, double maintenance, double equity, double geopolitics) {
    return 0.14 * (1.0 - centralization) + 0.18 * redundancy - 0.12 * digital - 0.16 * climate
        + 0.16 * coordination + 0.12 * finance + 0.12 * maintenance + 0.10 * equity
        - 0.08 * geopolitics;
}

int main() {
    std::cout << "Adaptive Public Infrastructure viability="
              << infrastructure_viability(0.46, 0.78, 0.58, 0.42, 0.78, 0.76, 0.80, 0.76, 0.38) << "\n";
    return 0;
}
