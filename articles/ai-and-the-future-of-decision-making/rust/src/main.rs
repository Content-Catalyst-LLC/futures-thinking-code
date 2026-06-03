fn decision_profile(human: f64, machine: f64, coordination: f64, transparency: f64, uncertainty: f64, accountability: f64, contestability: f64, equity: f64) -> f64 {
    0.16 * human + 0.16 * machine + 0.16 * coordination + 0.12 * transparency
        + 0.12 * uncertainty + 0.12 * accountability + 0.08 * contestability + 0.08 * equity
}

fn main() {
    let score = decision_profile(0.72, 0.74, 0.83, 0.79, 0.78, 0.82, 0.80, 0.76);
    println!("High-governance hybrid decision profile={:.4}", score);
}
