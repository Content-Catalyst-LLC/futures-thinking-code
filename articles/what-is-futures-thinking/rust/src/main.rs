fn robustness(values: &[f64]) -> f64 {
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let worst = values.iter().cloned().fold(f64::INFINITY, f64::min);
    let variance = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let volatility = variance.sqrt();
    0.45 * worst + 0.35 * mean - 0.20 * volatility
}

fn main() {
    println!("Futures diagnostics");
    println!("Flexible Foresight Strategy: robustness={:.4}", robustness(&[0.78, 0.75, 0.72, 0.70, 0.73, 0.69]));
}
