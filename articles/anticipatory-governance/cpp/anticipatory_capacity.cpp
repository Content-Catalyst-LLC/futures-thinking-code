#include <iostream>

double anticipatory_capacity(double detection, double interpretation, double scenario, double preparedness, double legitimacy, double coordination, double adaptive, double equity, double learning, double implementation) {
    return 0.12 * detection + 0.12 * interpretation + 0.12 * scenario + 0.12 * preparedness
        + 0.12 * legitimacy + 0.10 * coordination + 0.10 * adaptive + 0.08 * equity
        + 0.07 * learning + 0.05 * implementation;
}

int main() {
    std::cout << "Participatory Anticipatory Governance capacity="
              << anticipatory_capacity(0.68, 0.74, 0.78, 0.70, 0.86, 0.72, 0.68, 0.88, 0.78, 0.64) << "\n";
    return 0;
}
