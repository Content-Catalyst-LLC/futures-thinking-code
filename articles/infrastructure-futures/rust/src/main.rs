fn infrastructure_viability(centralization: f64, redundancy: f64, digital: f64, climate: f64, coordination: f64, finance: f64, maintenance: f64, equity: f64, geopolitics: f64) -> f64 {
    0.14 * (1.0 - centralization) + 0.18 * redundancy - 0.12 * digital - 0.16 * climate
        + 0.16 * coordination + 0.12 * finance + 0.12 * maintenance + 0.10 * equity
        - 0.08 * geopolitics
}

fn main() {
    let score = infrastructure_viability(0.46, 0.78, 0.58, 0.42, 0.78, 0.76, 0.80, 0.76, 0.38);
    println!("Adaptive Public Infrastructure viability={:.4}", score);
}
