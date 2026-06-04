fn financial_resilience(leverage: f64, liquidity: f64, household: f64, climate: f64, nonbank: f64, digital: f64, regulation: f64, public_finance: f64, consumer: f64, productive: f64) -> f64 {
    0.14 * liquidity + 0.14 * household + 0.14 * regulation + 0.10 * public_finance
        + 0.10 * consumer + 0.10 * productive + 0.10 * (1.0 - leverage)
        + 0.08 * (1.0 - climate) + 0.06 * (1.0 - nonbank) + 0.04 * (1.0 - digital)
}

fn main() {
    let score = financial_resilience(0.42, 0.82, 0.80, 0.44, 0.48, 0.38, 0.86, 0.78, 0.84, 0.76);
    println!("Resilient Public-Interest Finance resilience={:.4}", score);
}
