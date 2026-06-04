fn foresight_capability(signal: f64, scenario: f64, learning: f64, governance: f64, adaptive: f64, participation: f64, ethics: f64, data: f64) -> f64 {
    0.16 * signal + 0.16 * scenario + 0.14 * learning + 0.14 * governance
        + 0.12 * adaptive + 0.10 * participation + 0.10 * ethics + 0.08 * data
}

fn main() {
    let score = foresight_capability(0.76, 0.74, 0.72, 0.70, 0.66, 0.66, 0.72, 0.68);
    println!("Climate Adaptation Authority foresight_capability={:.4}", score);
}
