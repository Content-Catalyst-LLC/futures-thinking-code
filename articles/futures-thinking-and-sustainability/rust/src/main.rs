fn sustainability_viability(ecology: f64, equity: f64, adaptive: f64, technology: f64, governance: f64, finance: f64, resilience: f64, justice: f64, degradation: f64) -> f64 {
    0.17 * ecology + 0.15 * equity + 0.14 * adaptive + 0.10 * technology
        + 0.14 * governance + 0.10 * finance + 0.10 * resilience
        + 0.10 * justice - 0.08 * degradation
}

fn main() {
    let score = sustainability_viability(0.82, 0.82, 0.80, 0.70, 0.78, 0.76, 0.82, 0.86, 0.30);
    println!("Just Transformative Sustainability viability={:.4}", score);
}
