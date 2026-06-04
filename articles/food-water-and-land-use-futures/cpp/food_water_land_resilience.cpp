#include <iostream>

double fwl_resilience(double production, double water, double soil, double biodiversity, double governance, double climate, double market, double justice, double livelihoods) {
    return 0.13 * production + 0.16 * water + 0.15 * soil + 0.14 * biodiversity
        + 0.14 * governance - 0.12 * climate - 0.08 * market
        + 0.14 * justice + 0.12 * livelihoods;
}

int main() {
    std::cout << "Regenerative Transition resilience="
              << fwl_resilience(0.72, 0.76, 0.82, 0.78, 0.76, 0.42, 0.38, 0.80, 0.78) << "\n";
    return 0;
}
