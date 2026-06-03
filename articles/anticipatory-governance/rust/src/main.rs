fn anticipatory_capacity(detection: f64, interpretation: f64, scenario: f64, preparedness: f64, legitimacy: f64, coordination: f64, adaptive: f64, equity: f64, learning: f64, implementation: f64) -> f64 {
    0.12 * detection + 0.12 * interpretation + 0.12 * scenario + 0.12 * preparedness
        + 0.12 * legitimacy + 0.10 * coordination + 0.10 * adaptive + 0.08 * equity
        + 0.07 * learning + 0.05 * implementation
}

fn main() {
    let score = anticipatory_capacity(0.68, 0.74, 0.78, 0.70, 0.86, 0.72, 0.68, 0.88, 0.78, 0.64);
    println!("Participatory Anticipatory Governance capacity={:.4}", score);
}
