fn driver_priority(v: &[f64]) -> f64 {
    0.22 * v[0] + 0.20 * v[1] + 0.14 * v[2] + 0.14 * v[3]
        + 0.12 * v[4] + 0.08 * v[5] + 0.06 * v[6] + 0.04 * (1.0 - v[7])
}

fn main() {
    let public_trust = [0.88, 0.82, 0.80, 0.84, 0.84, 0.70, 0.68, 0.54];
    println!(
        "Public trust driver priority={:.4}",
        driver_priority(&public_trust)
    );
}
