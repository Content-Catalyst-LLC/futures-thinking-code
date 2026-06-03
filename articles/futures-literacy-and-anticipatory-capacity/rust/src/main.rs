fn weighted_score(values: &[f64], weights: &[f64]) -> f64 {
    values.iter().zip(weights.iter()).map(|(v, w)| v * w).sum()
}

fn main() {
    let values = [0.82, 0.84, 0.88, 0.90, 0.72, 0.84, 0.80];
    let weights = [0.15, 0.15, 0.17, 0.13, 0.17, 0.13, 0.10];
    println!(
        "Futures-Literate Organization anticipatory capacity={:.4}",
        weighted_score(&values, &weights)
    );
}
