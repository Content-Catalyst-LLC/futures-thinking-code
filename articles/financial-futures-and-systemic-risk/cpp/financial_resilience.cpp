#include <iostream>

double financial_resilience(double leverage, double liquidity, double household, double climate, double nonbank, double digital, double regulation, double public_finance, double consumer, double productive) {
    return 0.14 * liquidity + 0.14 * household + 0.14 * regulation + 0.10 * public_finance
        + 0.10 * consumer + 0.10 * productive + 0.10 * (1.0 - leverage)
        + 0.08 * (1.0 - climate) + 0.06 * (1.0 - nonbank) + 0.04 * (1.0 - digital);
}

int main() {
    std::cout << "Resilient Public-Interest Finance resilience="
              << financial_resilience(0.42, 0.82, 0.80, 0.44, 0.48, 0.38, 0.86, 0.78, 0.84, 0.76) << "\n";
    return 0;
}
