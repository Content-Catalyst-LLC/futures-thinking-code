fn health_resilience(prevention: f64, access: f64, public_health: f64, climate: f64, workforce: f64, tech: f64, social: f64, trust: f64, equity: f64, care: f64) -> f64 {
    0.13 * prevention + 0.12 * access + 0.15 * public_health + 0.10 * climate
        + 0.11 * workforce + 0.08 * tech + 0.11 * social + 0.08 * trust
        + 0.07 * equity + 0.05 * care
}

fn main() {
    let score = health_resilience(0.86, 0.84, 0.88, 0.78, 0.76, 0.78, 0.84, 0.82, 0.88, 0.80);
    println!("Equitable Health Systems Transformation resilience={:.4}", score);
}
