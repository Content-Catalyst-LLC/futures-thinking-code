fn ethical_profile(intergen: f64, inclusion: f64, accountability: f64, risk_equity: f64, transparency: f64, contestability: f64, precaution: f64, learning: f64, epistemic: f64, legitimacy: f64) -> f64 {
    0.13 * intergen + 0.12 * inclusion + 0.12 * accountability + 0.12 * risk_equity
        + 0.10 * transparency + 0.10 * contestability + 0.10 * precaution
        + 0.08 * learning + 0.08 * epistemic + 0.05 * legitimacy
}

fn main() {
    let score = ethical_profile(0.72, 0.84, 0.76, 0.82, 0.78, 0.80, 0.74, 0.72, 0.86, 0.82);
    println!("Civil Society Coalition ethical_futures_profile={:.4}", score);
}
