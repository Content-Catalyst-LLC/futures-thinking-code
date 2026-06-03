fn cla_depth(v: &[f64]) -> f64 {
    0.10 * v[0] + 0.18 * v[1] + 0.22 * v[2] + 0.20 * v[3] + 0.16 * v[4] + 0.08 * v[5] + 0.06 * v[6]
}

fn main() {
    let climate_housing = [0.90, 0.88, 0.84, 0.86, 0.88, 0.94, 0.92];
    println!(
        "Climate adaptation and housing CLA depth={:.4}",
        cla_depth(&climate_housing)
    );
}
