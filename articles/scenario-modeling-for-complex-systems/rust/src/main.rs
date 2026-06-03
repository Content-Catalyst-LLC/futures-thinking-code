fn viability(v: &[f64]) -> f64 {
    0.35 * v[0] + 0.30 * v[1] + 0.20 * v[2] + 0.15 * v[3]
}

fn main() {
    let robust_resilience = [1.55, 1.02, 1.28, 0.15];
    println!(
        "Robust resilience portfolio viability={:.4}",
        viability(&robust_resilience)
    );
}
