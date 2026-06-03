#include <stdio.h>

double judgment_profile(double v[]) {
    return 0.25 * v[0] + 0.35 * v[1] + 0.25 * v[2] + 0.15 * v[3];
}

int main(void) {
    double public_ai[] = {0.69, 0.92, 0.87, 0.61};
    printf("Public AI accountability Delphi judgment profile: %.4f\n", judgment_profile(public_ai));
    return 0;
}
