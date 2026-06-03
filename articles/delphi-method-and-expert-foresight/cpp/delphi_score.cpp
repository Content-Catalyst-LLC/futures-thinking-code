#include <iostream>
#include <vector>

double judgment_profile(const std::vector<double>& v) {
    return 0.25 * v[0] + 0.35 * v[1] + 0.25 * v[2] + 0.15 * v[3];
}

int main() {
    std::vector<double> public_ai = {0.69, 0.92, 0.87, 0.61};
    std::cout << "Public AI accountability Delphi judgment profile="
              << judgment_profile(public_ai) << "\n";
    return 0;
}
