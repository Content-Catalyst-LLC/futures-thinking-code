fn warning_score(v: &[f64]) -> f64 {
    0.12 * v[0]
        + 0.22 * v[1]
        + 0.20 * v[2]
        + 0.13 * v[3]
        + 0.11 * v[4]
        + 0.13 * v[5]
        + 0.09 * v[6]
}

fn main() {
    let heat_health = [0.58, 0.90, 0.88, 0.82, 0.68, 0.92, 0.80];
    println!(
        "Rising heat-health emergency demand warning score={:.4}",
        warning_score(&heat_health)
    );
}
