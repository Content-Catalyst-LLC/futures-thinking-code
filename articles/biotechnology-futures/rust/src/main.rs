fn responsible_capacity(science: f64, governance: f64, legitimacy: f64, equity: f64, manufacturing: f64, consent: f64, ecology_uncertainty: f64, dual_use_risk: f64) -> f64 {
    0.16 * science + 0.18 * governance + 0.16 * legitimacy + 0.16 * equity
        + 0.12 * manufacturing + 0.12 * consent + 0.05 * (1.0 - ecology_uncertainty) + 0.05 * (1.0 - dual_use_risk)
}

fn main() {
    let score = responsible_capacity(0.68, 0.82, 0.84, 0.86, 0.62, 0.88, 0.46, 0.34);
    println!("Democratic Biofutures responsible biotechnology capacity={:.4}", score);
}
