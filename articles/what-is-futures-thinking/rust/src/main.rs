fn robustness(values: &[f64], adaptability: f64, equity: f64, difficulty: f64) -> f64 {
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let worst = values.iter().cloned().fold(f64::INFINITY, f64::min);
    let variance = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let volatility = variance.sqrt();
    0.45 * worst + 0.30 * mean + 0.15 * adaptability + 0.10 * equity - 0.15 * volatility - 0.05 * difficulty
}

fn main() {
    let strategies = vec![
        ("Forecast-Optimized Strategy", vec![0.91, 0.42, 0.38, 0.36, 0.49], 0.28, 0.32, 0.34),
        ("Flexible Foresight Strategy", vec![0.78, 0.76, 0.74, 0.71, 0.79], 0.84, 0.72, 0.58),
        ("Transformational Strategy", vec![0.62, 0.82, 0.85, 0.77, 0.88], 0.78, 0.88, 0.82),
        ("Participatory Futures Strategy", vec![0.66, 0.72, 0.78, 0.80, 0.86], 0.74, 0.92, 0.66),
    ];

    println!("strategy,robustness");
    for (name, values, adaptability, equity, difficulty) in strategies {
        println!("{}, {:.4}", name, robustness(&values, adaptability, equity, difficulty));
    }
}
