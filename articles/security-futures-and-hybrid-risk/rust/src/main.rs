fn hybrid_risk(cyber: f64, infra: f64, info: f64, climate: f64, resource: f64, coordination: f64, protection: f64, adaptive: f64, trust: f64, attribution: f64) -> f64 {
    0.13 * cyber + 0.13 * infra + 0.13 * info + 0.12 * climate + 0.10 * resource
        + 0.11 * (1.0 - coordination) + 0.10 * (1.0 - protection)
        + 0.10 * (1.0 - adaptive) + 0.05 * (1.0 - trust) + 0.03 * (1.0 - attribution)
}

fn main() {
    let score = hybrid_risk(0.88, 0.92, 0.90, 0.88, 0.84, 0.22, 0.20, 0.18, 0.16, 0.22);
    println!("Systemic Security Breakdown hybrid_risk={:.4}", score);
}
