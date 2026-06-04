#include <iostream>

double foresight_capability(double signal, double scenario, double learning, double governance, double adaptive, double participation, double ethics, double data) {
    return 0.16 * signal + 0.16 * scenario + 0.14 * learning + 0.14 * governance
        + 0.12 * adaptive + 0.10 * participation + 0.10 * ethics + 0.08 * data;
}

int main() {
    std::cout << "Climate Adaptation Authority foresight_capability="
              << foresight_capability(0.76, 0.74, 0.72, 0.70, 0.66, 0.66, 0.72, 0.68) << "\n";
    return 0;
}
