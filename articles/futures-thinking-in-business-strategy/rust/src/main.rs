fn futures_readiness(innovation: f64, exposure: f64, resilience: f64, flexibility: f64, alignment: f64, sensing: f64, capital: f64, legitimacy: f64, transition: f64) -> f64 {
    0.14 * innovation - 0.10 * exposure + 0.15 * resilience + 0.14 * flexibility
        + 0.10 * alignment + 0.12 * sensing + 0.08 * capital + 0.09 * legitimacy + 0.08 * transition
}

fn main() {
    let score = futures_readiness(0.82, 0.52, 0.72, 0.79, 0.68, 0.80, 0.66, 0.70, 0.76);
    println!("Adaptive Innovation Strategy readiness={:.4}", score);
}
