fn consumer_future_health(affordability: f64, trust: f64, digital: f64, sustainability: f64, access: f64, price: f64, friction: f64, regulation: f64, privacy: f64, local: f64) -> f64 {
    0.14 * affordability + 0.16 * trust + 0.10 * sustainability + 0.16 * access
        + 0.10 * (1.0 - price) + 0.12 * (1.0 - friction) + 0.06 * digital
        + 0.06 * regulation + 0.06 * privacy + 0.04 * local
}

fn main() {
    let score = consumer_future_health(0.70, 0.76, 0.66, 0.70, 0.86, 0.70, 0.42, 0.68, 0.70, 0.76);
    println!("Access and Inclusion Market health={:.4}", score);
}
