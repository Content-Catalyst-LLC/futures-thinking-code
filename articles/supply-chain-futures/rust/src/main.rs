fn resilience_score(cost: f64, diversification: f64, buffer: f64, visibility: f64, labor: f64, climate: f64, traceability: f64, circularity: f64, regulation: f64, recovery: f64) -> f64 {
    0.10 * cost + 0.16 * diversification + 0.14 * buffer + 0.14 * visibility
        + 0.12 * labor + 0.13 * climate + 0.09 * traceability + 0.06 * circularity
        + 0.04 * regulation + 0.02 * recovery
}

fn main() {
    let score = resilience_score(0.52, 0.76, 0.84, 0.74, 0.72, 0.70, 0.76, 0.54, 0.80, 0.86);
    println!("Essential Goods Resilience Model resilience={:.4}", score);
}
