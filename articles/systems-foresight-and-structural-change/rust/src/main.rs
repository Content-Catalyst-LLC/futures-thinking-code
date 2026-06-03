fn structural_pressure(v: &[f64]) -> f64 {
    0.26 * v[0] + 0.22 * (1.0 - v[1]) + 0.18 * (1.0 - v[2]) + 0.18 * v[3] + 0.16 * v[4]
}

fn main() {
    let climate_adaptation = [0.86, 0.46, 0.52, 0.88, 0.90];
    println!(
        "Climate adaptation structural pressure={:.4}",
        structural_pressure(&climate_adaptation)
    );
}
