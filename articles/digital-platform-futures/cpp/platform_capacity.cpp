#include <iostream>

double public_interest_capacity(double platform_power, double data_advantage, double interoperability, double worker_protection, double public_accountability, double user_rights, double ecological_responsibility, double digital_public_value) {
    return 0.18 * interoperability + 0.18 * public_accountability + 0.16 * user_rights
        + 0.14 * worker_protection + 0.14 * digital_public_value + 0.10 * ecological_responsibility
        + 0.05 * (1.0 - platform_power) + 0.05 * (1.0 - data_advantage);
}

int main() {
    std::cout << "Digital Public Infrastructure Turn public-interest platform capacity="
              << public_interest_capacity(0.42, 0.46, 0.76, 0.70, 0.82, 0.84, 0.70, 0.86) << "\n";
    return 0;
}
