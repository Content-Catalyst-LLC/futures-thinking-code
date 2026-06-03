fn democratic_capacity(inclusion: f64, deliberation: f64, representation: f64, uptake: f64, accountability: f64, justice: f64, learning: f64, influence: f64, accessibility: f64, authority: f64) -> f64 {
    0.11 * inclusion + 0.12 * deliberation + 0.11 * representation + 0.14 * uptake
        + 0.12 * accountability + 0.12 * justice + 0.08 * learning + 0.10 * influence
        + 0.05 * accessibility + 0.05 * authority
}

fn main() {
    let score = democratic_capacity(0.82, 0.78, 0.80, 0.78, 0.82, 0.84, 0.78, 0.80, 0.76, 0.86);
    println!("Co-Governance Futures Board capacity={:.4}", score);
}
