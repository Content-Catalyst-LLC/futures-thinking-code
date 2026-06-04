#include <iostream>

double coloniality_risk(double agenda, double consent, double land, double external, double epistemic, double benefit, double harm, double repair, double sovereignty, double data, double labor) {
    return 0.12 * agenda + 0.12 * (1.0 - consent) + 0.12 * land + 0.12 * external
        + 0.11 * (1.0 - epistemic) + 0.10 * (1.0 - benefit) + 0.10 * harm
        + 0.09 * (1.0 - repair) + 0.07 * (1.0 - sovereignty)
        + 0.03 * (1.0 - data) + 0.02 * (1.0 - labor);
}

int main() {
    std::cout << "Green Extraction Continuity coloniality_risk="
              << coloniality_risk(0.86, 0.34, 0.90, 0.82, 0.36, 0.38, 0.78, 0.24, 0.30, 0.28, 0.44) << "\n";
    return 0;
}
