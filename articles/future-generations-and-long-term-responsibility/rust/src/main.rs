fn inherited_burden(climate: f64, debt: f64, infrastructure: f64, ecology: f64, institution: f64, tech_lock: f64, adaptive: f64, representation: f64) -> f64 {
    0.18 * climate + 0.14 * debt + 0.16 * infrastructure + 0.18 * ecology + 0.14 * tech_lock
        + 0.10 * (1.0 - institution) + 0.06 * (1.0 - adaptive) + 0.04 * (1.0 - representation)
}

fn main() {
    let score = inherited_burden(0.88, 0.76, 0.70, 0.84, 0.38, 0.62, 0.36, 0.24);
    println!("Short-Term Extraction inherited_burden={:.4}", score);
}
