#include <iostream>

double demographic_stress(double aging, double youth, double migration, double care, double housing, double labor, double climate, double cohesion, double gender, double health) {
    return 0.13 * aging + 0.13 * youth + 0.12 * migration + 0.13 * (1.0 - care) + 0.12 * housing
        + 0.10 * (1.0 - labor) + 0.11 * climate + 0.08 * (1.0 - cohesion)
        + 0.05 * (1.0 - gender) + 0.03 * (1.0 - health);
}

int main() {
    std::cout << "Demographic Fear Politics stress="
              << demographic_stress(0.62, 0.70, 0.80, 0.34, 0.74, 0.36, 0.62, 0.22, 0.28, 0.38) << "\n";
    return 0;
}
