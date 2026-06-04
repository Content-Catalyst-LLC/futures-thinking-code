fn climate_readiness(emissions: f64, adaptation: f64, ecosystem: f64, governance: f64, vulnerability: f64, technology: f64, transition: f64, justice: f64, residual_loss: f64) -> f64 {
    -0.16 * emissions + 0.15 * adaptation - 0.15 * ecosystem + 0.14 * governance
        - 0.12 * vulnerability + 0.10 * technology + 0.14 * transition
        + 0.12 * justice - 0.10 * residual_loss
}

fn main() {
    let score = climate_readiness(0.26, 0.78, 0.34, 0.78, 0.34, 0.70, 0.76, 0.82, 0.28);
    println!("Just Climate Transformation readiness={:.4}", score);
}
