fn foresight_capacity(scanning: f64, scenarios: f64, uptake: f64, participation: f64, budget: f64, evaluation: f64, learning: f64, authority: f64, knowledge: f64, legitimacy: f64) -> f64 {
    0.12 * scanning + 0.12 * scenarios + 0.14 * uptake + 0.12 * participation
        + 0.12 * budget + 0.10 * evaluation + 0.10 * learning + 0.10 * authority
        + 0.05 * knowledge + 0.03 * legitimacy
}

fn main() {
    let score = foresight_capacity(0.68, 0.78, 0.68, 0.90, 0.62, 0.76, 0.80, 0.60, 0.72, 0.86);
    println!("Participatory Public Foresight System capacity={:.4}", score);
}
