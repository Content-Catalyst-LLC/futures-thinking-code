fn futures_risk(probability: f64, structural: f64, interdependence: f64, vulnerability: f64, resilience: f64, governance: f64, signal: f64, tail: f64, distributional: f64, adaptive: f64) -> f64 {
    0.12 * (1.0 - probability) + 0.16 * structural + 0.14 * interdependence + 0.15 * vulnerability
        - 0.11 * resilience - 0.10 * governance - 0.08 * signal + 0.12 * tail
        + 0.10 * distributional - 0.02 * adaptive
}

fn main() {
    let score = futures_risk(0.18, 0.88, 0.91, 0.84, 0.31, 0.28, 0.26, 0.94, 0.92, 0.30);
    println!("Systemic Cascade futures_risk_score={:.4}", score);
}
