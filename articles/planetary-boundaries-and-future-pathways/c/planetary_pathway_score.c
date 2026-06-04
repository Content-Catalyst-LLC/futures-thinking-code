#include <stdio.h>

double boundary_pressure(double climate, double biosphere, double land, double freshwater, double nutrient, double ocean, double aerosol, double novel, double technology) {
    return 0.16 * climate + 0.16 * biosphere + 0.12 * land + 0.12 * freshwater
        + 0.10 * nutrient + 0.10 * ocean + 0.08 * aerosol + 0.10 * novel
        + 0.06 * technology;
}

double safe_just_score(double social, double governance, double justice, double regeneration, double pressure, double technology) {
    return 0.22 * social + 0.20 * governance + 0.20 * justice + 0.14 * regeneration - 0.20 * pressure + 0.04 * (1.0 - technology);
}

int main(void) {
    double pressure = boundary_pressure(0.32, 0.30, 0.34, 0.30, 0.32, 0.34, 0.30, 0.36, 0.56);
    double score = safe_just_score(0.82, 0.80, 0.84, 0.78, pressure, 0.56);
    printf("Safe and Just Transformation boundary_pressure=%.4f safe_and_just_score=%.4f\n", pressure, score);
    return 0;
}
