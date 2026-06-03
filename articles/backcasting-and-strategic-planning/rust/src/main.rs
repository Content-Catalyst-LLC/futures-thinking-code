fn pathway_viability(v: &[f64]) -> f64 {
    0.18 * v[0] - 0.16 * v[1] + 0.14 * v[2] + 0.18 * v[3] + 0.16 * v[4] + 0.12 * v[5] + 0.14 * v[6] - 0.12 * v[7]
}

fn main() {
    let public_accountability = [0.66, 0.56, 0.52, 0.78, 0.72, 0.86, 0.80, 0.40];
    println!(
        "Public Accountability Before Scale viability={:.4}",
        pathway_viability(&public_accountability)
    );
}
