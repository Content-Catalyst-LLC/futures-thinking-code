#include <iostream>

double foresight_capacity(double scanning, double scenarios, double uptake, double participation, double budget, double evaluation, double learning, double authority, double knowledge, double legitimacy) {
    return 0.12 * scanning + 0.12 * scenarios + 0.14 * uptake + 0.12 * participation
        + 0.12 * budget + 0.10 * evaluation + 0.10 * learning + 0.10 * authority
        + 0.05 * knowledge + 0.03 * legitimacy;
}

int main() {
    std::cout << "Participatory Public Foresight System capacity="
              << foresight_capacity(0.68, 0.78, 0.68, 0.90, 0.62, 0.76, 0.80, 0.60, 0.72, 0.86) << "\n";
    return 0;
}
