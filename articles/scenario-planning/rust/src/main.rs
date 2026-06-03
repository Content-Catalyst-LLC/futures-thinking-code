fn robustness(values: &[f64]) -> f64 {
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let worst = values.iter().cloned().fold(f64::INFINITY, f64::min);
    let variance = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let volatility = variance.sqrt();
    0.55 * worst + 0.35 * mean - 0.10 * volatility
}

fn main() {
    let values = [0.74, 0.76, 0.73, 0.70, 0.80];
    println!("Robust Adaptive Strategy robustness={:.4}", robustness(&values));
}
