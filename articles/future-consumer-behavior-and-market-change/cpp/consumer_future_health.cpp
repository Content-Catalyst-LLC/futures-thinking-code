#include <iostream>

double consumer_future_health(double affordability, double trust, double digital, double sustainability, double access, double price, double friction, double regulation, double privacy, double local) {
    return 0.14 * affordability + 0.16 * trust + 0.10 * sustainability + 0.16 * access
        + 0.10 * (1.0 - price) + 0.12 * (1.0 - friction) + 0.06 * digital
        + 0.06 * regulation + 0.06 * privacy + 0.04 * local;
}

int main() {
    std::cout << "Access and Inclusion Market health="
              << consumer_future_health(0.70, 0.76, 0.66, 0.70, 0.86, 0.70, 0.42, 0.68, 0.70, 0.76) << "\n";
    return 0;
}
