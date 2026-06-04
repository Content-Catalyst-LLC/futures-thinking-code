#include <iostream>

double hybrid_risk(double cyber, double infra, double info, double climate, double resource, double coordination, double protection, double adaptive, double trust, double attribution) {
    return 0.13 * cyber + 0.13 * infra + 0.13 * info + 0.12 * climate + 0.10 * resource
        + 0.11 * (1.0 - coordination) + 0.10 * (1.0 - protection)
        + 0.10 * (1.0 - adaptive) + 0.05 * (1.0 - trust) + 0.03 * (1.0 - attribution);
}

int main() {
    std::cout << "Systemic Security Breakdown hybrid_risk="
              << hybrid_risk(0.88, 0.92, 0.90, 0.88, 0.84, 0.22, 0.20, 0.18, 0.16, 0.22) << "\n";
    return 0;
}
