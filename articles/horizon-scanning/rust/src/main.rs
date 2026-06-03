fn horizon_profile(v: &[f64]) -> f64 {
    0.10 * v[0] - 0.08 * v[1] + 0.22 * v[2] + 0.18 * v[3] + 0.14 * v[4] + 0.14 * v[5] + 0.30 * v[6]
}

fn main() {
    let climate_insurance = [0.48, 0.57, 0.90, 0.82, 0.72, 0.84, 0.91];
    println!(
        "Climate insurance withdrawal signal profile={:.4}",
        horizon_profile(&climate_insurance)
    );
}
