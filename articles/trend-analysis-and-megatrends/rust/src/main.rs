fn trend_profile(v: &[f64]) -> f64 {
    0.20 * v[0] + 0.22 * v[1] + 0.22 * v[2] - 0.12 * v[3] - 0.14 * v[4] + 0.10 * v[5]
}

fn main() {
    let climate_risk = [0.74, 0.86, 0.88, 0.22, 0.52, 0.86];
    println!(
        "Climate Risk Intensification profile={:.4}",
        trend_profile(&climate_risk)
    );
}
