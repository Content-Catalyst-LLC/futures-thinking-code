fn fwl_resilience(production: f64, water: f64, soil: f64, biodiversity: f64, governance: f64, climate: f64, market: f64, justice: f64, livelihoods: f64) -> f64 {
    0.13 * production + 0.16 * water + 0.15 * soil + 0.14 * biodiversity
        + 0.14 * governance - 0.12 * climate - 0.08 * market
        + 0.14 * justice + 0.12 * livelihoods
}

fn main() {
    let score = fwl_resilience(0.72, 0.76, 0.82, 0.78, 0.76, 0.42, 0.38, 0.80, 0.78);
    println!("Regenerative Transition resilience={:.4}", score);
}
