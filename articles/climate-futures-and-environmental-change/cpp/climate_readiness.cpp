#include <iostream>

double climate_readiness(double emissions, double adaptation, double ecosystem, double governance, double vulnerability, double technology, double transition, double justice, double residual_loss) {
    return -0.16 * emissions + 0.15 * adaptation - 0.15 * ecosystem + 0.14 * governance
        - 0.12 * vulnerability + 0.10 * technology + 0.14 * transition
        + 0.12 * justice - 0.10 * residual_loss;
}

int main() {
    std::cout << "Just Climate Transformation readiness="
              << climate_readiness(0.26, 0.78, 0.34, 0.78, 0.34, 0.70, 0.76, 0.82, 0.28) << "\n";
    return 0;
}
