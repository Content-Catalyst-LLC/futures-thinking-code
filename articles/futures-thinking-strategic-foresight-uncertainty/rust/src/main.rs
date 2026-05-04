fn robustness_score(values: &[f64]) -> f64 {
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let worst = values.iter().cloned().fold(f64::INFINITY, f64::min);
    let best = values.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let range = best - worst;

    0.50 * worst + 0.30 * mean - 0.20 * range
}

fn main() {
    let strategy_values = vec![0.72, 0.78, 0.74, 0.73, 0.69, 0.80];

    println!("Futures Thinking CLI");
    println!("Futures-oriented strategy robustness score: {:.3}", robustness_score(&strategy_values));
    println!("Interpretation: this is a conceptual readiness diagnostic, not a forecast.");
}
