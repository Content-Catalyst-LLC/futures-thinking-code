#include <iostream>

double job_quality(double wage_security, double worker_voice, double training, double protection, double surveillance, double initial_quality) {
    return 0.28 * initial_quality + 0.18 * wage_security + 0.18 * worker_voice
        + 0.16 * protection + 0.12 * training + 0.08 * (1.0 - surveillance);
}

int main() {
    std::cout << "Knowledge work adjusted job quality="
              << job_quality(0.66, 0.54, 0.72, 0.60, 0.46, 0.70) << "\n";
    return 0;
}
