#include <stdio.h>

double reflective_score(double methodological, double participation, double ethics, double systems) {
    return 0.25 * methodological + 0.25 * participation + 0.25 * ethics + 0.25 * systems;
}

double power_risk(double institutional_power, double participation, double ethics) {
    return institutional_power * (1.0 - participation) * (1.0 - ethics);
}

int main(void) {
    double score = reflective_score(0.68, 0.92, 0.86, 0.64);
    double risk = power_risk(0.42, 0.92, 0.86);
    printf("Participatory and Democratic Futures: reflective_score=%.4f power_risk=%.4f\n", score, risk);
    return 0;
}
