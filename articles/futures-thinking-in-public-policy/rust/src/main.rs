fn policy_futures_profile(robustness: f64, equity: f64, adaptability: f64, coordination: f64, legitimacy: f64, implementation: f64, learning: f64, intergenerational: f64) -> f64 {
    0.20 * robustness + 0.16 * equity + 0.18 * adaptability + 0.14 * coordination
        + 0.14 * legitimacy + 0.08 * implementation + 0.06 * learning + 0.04 * intergenerational
}

fn main() {
    let score = policy_futures_profile(0.80, 0.84, 0.82, 0.76, 0.86, 0.56, 0.82, 0.84);
    println!("Participatory Anticipatory Policy futures profile={:.4}", score);
}
