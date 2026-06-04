#include <iostream>

double urban_viability(double infrastructure, double governance, double housing, double climate, double inequality, double digital, double finance, double cohesion, double maintenance) {
    return 0.17 * infrastructure + 0.16 * governance + 0.14 * housing - 0.14 * climate
        - 0.14 * inequality + 0.09 * digital + 0.12 * finance + 0.14 * cohesion
        - 0.08 * maintenance;
}

int main() {
    std::cout << "Adaptive Public City viability="
              << urban_viability(0.78, 0.78, 0.74, 0.42, 0.40, 0.68, 0.76, 0.74, 0.34) << "\n";
    return 0;
}
