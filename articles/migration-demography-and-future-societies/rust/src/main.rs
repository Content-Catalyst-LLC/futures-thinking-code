fn demographic_stress(aging: f64, youth: f64, migration: f64, care: f64, housing: f64, labor: f64, climate: f64, cohesion: f64, gender: f64, health: f64) -> f64 {
    0.13 * aging + 0.13 * youth + 0.12 * migration + 0.13 * (1.0 - care) + 0.12 * housing
        + 0.10 * (1.0 - labor) + 0.11 * climate + 0.08 * (1.0 - cohesion)
        + 0.05 * (1.0 - gender) + 0.03 * (1.0 - health)
}

fn main() {
    let score = demographic_stress(0.62, 0.70, 0.80, 0.34, 0.74, 0.36, 0.62, 0.22, 0.28, 0.38);
    println!("Demographic Fear Politics stress={:.4}", score);
}
