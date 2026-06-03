#include <stdio.h>

double regulatory_capacity(double foresight, double monitoring, double enforcement, double rights, double participation, double revision, double learning, double capture, double certainty, double remedy) {
    return 0.13 * foresight + 0.12 * monitoring + 0.12 * enforcement + 0.14 * rights
        + 0.10 * participation + 0.12 * revision + 0.10 * learning + 0.08 * capture
        + 0.05 * certainty + 0.04 * remedy;
}

int main(void) {
    printf("Rights-Centered Technology Regulation capacity: %.4f\n",
           regulatory_capacity(0.70, 0.76, 0.78, 0.90, 0.62, 0.72, 0.74, 0.72, 0.66, 0.86));
    return 0;
}
