#include <iostream>

double disciplined_hope(double hope, double agency, double trust, double institution, double accountability, double repair, double fatigue, double polarization) {
    return 0.18 * hope + 0.18 * agency + 0.16 * trust + 0.16 * institution
        + 0.14 * accountability + 0.12 * repair - 0.04 * fatigue - 0.02 * polarization;
}

int main() {
    std::cout << "Reparative Imagination disciplined_hope="
              << disciplined_hope(0.86, 0.84, 0.76, 0.80, 0.88, 0.92, 0.28, 0.30) << "\n";
    return 0;
}
