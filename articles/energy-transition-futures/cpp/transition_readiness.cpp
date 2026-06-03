#include <iostream>

double transition_readiness(double clean, double grid, double storage, double electrification, double phase_down, double justice, double labor, double materials, double resilience) {
    return 0.14 * clean + 0.14 * grid + 0.12 * storage + 0.12 * electrification
        + 0.12 * phase_down + 0.12 * justice + 0.10 * labor + 0.08 * materials + 0.06 * resilience;
}

int main() {
    std::cout << "Managed Just Transition readiness="
              << transition_readiness(0.82, 0.78, 0.74, 0.76, 0.78, 0.84, 0.82, 0.76, 0.80) << "\n";
    return 0;
}
