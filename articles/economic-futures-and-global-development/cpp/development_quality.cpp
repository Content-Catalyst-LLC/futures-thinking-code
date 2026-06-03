#include <iostream>

double development_quality(double growth, double inequality, double ecology, double institutions, double resilience, double fiscal, double labor, double public_investment, double tech, double trade, double legitimacy) {
    return 0.14 * growth - 0.12 * inequality - 0.14 * ecology + 0.13 * institutions
        + 0.12 * resilience + 0.08 * fiscal + 0.08 * labor + 0.08 * public_investment
        + 0.06 * tech + 0.03 * trade + 0.02 * legitimacy;
}

int main() {
    std::cout << "Green Coordinated Transition development_quality="
              << development_quality(0.64, 0.42, 0.36, 0.76, 0.79, 0.68, 0.70, 0.78, 0.68, 0.72, 0.70) << "\n";
    return 0;
}
