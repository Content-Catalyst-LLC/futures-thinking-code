fn governance_capacity(institutional: f64, legitimacy: f64, law: f64, finance: f64, collective: f64, tech: f64, planetary: f64, adaptive: f64, accountability: f64, representation: f64) -> f64 {
    0.14 * institutional + 0.16 * legitimacy + 0.12 * law + 0.11 * finance + 0.13 * collective
        + 0.10 * tech + 0.10 * planetary + 0.08 * adaptive + 0.08 * accountability + 0.08 * representation
}

fn main() {
    let score = governance_capacity(0.82, 0.88, 0.78, 0.80, 0.84, 0.78, 0.86, 0.88, 0.90, 0.92);
    println!("Democratic Justice Governance capacity={:.4}", score);
}
