fn boundary_pressure(climate: f64, biosphere: f64, land: f64, freshwater: f64, nutrient: f64, ocean: f64, aerosol: f64, novel: f64, technology: f64) -> f64 {
    0.16 * climate + 0.16 * biosphere + 0.12 * land + 0.12 * freshwater
        + 0.10 * nutrient + 0.10 * ocean + 0.08 * aerosol + 0.10 * novel
        + 0.06 * technology
}

fn safe_just_score(social: f64, governance: f64, justice: f64, regeneration: f64, pressure: f64, technology: f64) -> f64 {
    0.22 * social + 0.20 * governance + 0.20 * justice + 0.14 * regeneration - 0.20 * pressure + 0.04 * (1.0 - technology)
}

fn main() {
    let pressure = boundary_pressure(0.32, 0.30, 0.34, 0.30, 0.32, 0.34, 0.30, 0.36, 0.56);
    let score = safe_just_score(0.82, 0.80, 0.84, 0.78, pressure, 0.56);
    println!("Safe and Just Transformation boundary_pressure={:.4} safe_and_just_score={:.4}", pressure, score);
}
