fn development_quality(growth: f64, inequality: f64, ecology: f64, institutions: f64, resilience: f64, fiscal: f64, labor: f64, public_investment: f64, tech: f64, trade: f64, legitimacy: f64) -> f64 {
    0.14 * growth - 0.12 * inequality - 0.14 * ecology + 0.13 * institutions
        + 0.12 * resilience + 0.08 * fiscal + 0.08 * labor + 0.08 * public_investment
        + 0.06 * tech + 0.03 * trade + 0.02 * legitimacy
}

fn main() {
    let score = development_quality(0.64, 0.42, 0.36, 0.76, 0.79, 0.68, 0.70, 0.78, 0.68, 0.72, 0.70);
    println!("Green Coordinated Transition development_quality={:.4}", score);
}
