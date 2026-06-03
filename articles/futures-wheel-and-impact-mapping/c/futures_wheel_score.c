#include <stdio.h>

double consequence_priority(double v[]) {
    return 0.22 * v[0] + 0.26 * v[1] + 0.14 * v[2] + 0.22 * v[3] + 0.16 * v[4];
}

int main(void) {
    double heat_health[] = {0.84, 0.90, 0.36, 0.94, 0.78};
    printf("Heat-related health emergencies consequence priority: %.4f\n", consequence_priority(heat_health));
    return 0;
}
