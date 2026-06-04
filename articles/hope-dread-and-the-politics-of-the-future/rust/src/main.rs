fn disciplined_hope(hope: f64, agency: f64, trust: f64, institution: f64, accountability: f64, repair: f64, fatigue: f64, polarization: f64) -> f64 {
    0.18 * hope + 0.18 * agency + 0.16 * trust + 0.16 * institution
        + 0.14 * accountability + 0.12 * repair - 0.04 * fatigue - 0.02 * polarization
}

fn main() {
    let score = disciplined_hope(0.86, 0.84, 0.76, 0.80, 0.88, 0.92, 0.28, 0.30);
    println!("Reparative Imagination disciplined_hope={:.4}", score);
}
