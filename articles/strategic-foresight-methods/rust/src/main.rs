fn weighted_score(values: &[f64], weights: &[f64]) -> f64 {
    values.iter().zip(weights.iter()).map(|(v, w)| v * w).sum()
}

fn main() {
    let scenario_planning = [0.42, 0.82, 0.84, 0.72, 0.62, 0.76, 0.86];
    let weights = [0.16, 0.14, 0.16, 0.18, 0.14, 0.10, 0.12];
    println!(
        "Scenario Planning foresight method profile={:.4}",
        weighted_score(&scenario_planning, &weights)
    );
}
