fn future_scores(v: &[f64]) -> (f64, f64, f64, f64) {
    let plausibility = 0.40 * v[0] + 0.35 * v[1] + 0.25 * v[2];
    let probability = 0.70 * v[3] + 0.30 * v[0];
    let preference = 0.30 * v[4] + 0.25 * v[5] + 0.25 * v[6] + 0.20 * v[7];
    let priority = 0.35 * plausibility + 0.25 * probability + 0.40 * preference;
    (plausibility, probability, preference, priority)
}

fn main() {
    let values = [0.62, 0.70, 0.56, 0.42, 0.86, 0.78, 0.84, 0.90];
    let (plausibility, probability, preference, priority) = future_scores(&values);
    println!(
        "Participatory Anticipatory Governance: plausibility={:.4}, probability={:.4}, preference={:.4}, priority={:.4}",
        plausibility, probability, preference, priority
    );
}
