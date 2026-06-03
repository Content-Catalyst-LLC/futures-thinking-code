fn robustness(values: &[f64]) -> f64 {
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let worst = values.iter().cloned().fold(f64::INFINITY, f64::min);
    let variance = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let volatility = variance.sqrt();
    0.45 * worst + 0.35 * mean - 0.20 * volatility
}

fn main() {
    let strategies = vec![
        ("Forecast-Optimized Strategy", vec![0.91, 0.42, 0.38, 0.36, 0.40, 0.34]),
        ("Flexible Foresight Strategy", vec![0.78, 0.75, 0.72, 0.70, 0.73, 0.69]),
        ("Transformational Strategy", vec![0.62, 0.81, 0.84, 0.76, 0.78, 0.74]),
        ("Defensive Continuity Strategy", vec![0.70, 0.52, 0.55, 0.58, 0.57, 0.60]),
    ];

    println!("Forecasting, foresight, and futures studies diagnostics");
    for (name, values) in strategies {
        println!("{}: robustness={:.4}", name, robustness(&values));
    }
}
