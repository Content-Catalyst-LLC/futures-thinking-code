#include <iostream>

double sustainability_viability(double ecology, double equity, double adaptive, double technology, double governance, double finance, double resilience, double justice, double degradation) {
    return 0.17 * ecology + 0.15 * equity + 0.14 * adaptive + 0.10 * technology
        + 0.14 * governance + 0.10 * finance + 0.10 * resilience
        + 0.10 * justice - 0.08 * degradation;
}

int main() {
    std::cout << "Just Transformative Sustainability viability="
              << sustainability_viability(0.82, 0.82, 0.80, 0.70, 0.78, 0.76, 0.82, 0.86, 0.30) << "\n";
    return 0;
}
