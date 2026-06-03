fn adaptive_profile(learning: f64, flexibility: f64, coordination: f64, legitimacy: f64, feedback: f64, resources: f64, shock: f64, rigidity: f64, intergenerational: f64) -> f64 {
    0.18 * learning + 0.16 * flexibility + 0.16 * coordination + 0.14 * legitimacy
        + 0.14 * feedback + 0.10 * resources + 0.08 * shock - 0.10 * rigidity + 0.04 * intergenerational
}

fn main() {
    let score = adaptive_profile(0.72, 0.68, 0.66, 0.86, 0.76, 0.54, 0.70, 0.40, 0.82);
    println!("Participatory Governance Assembly adaptive profile={:.4}", score);
}
