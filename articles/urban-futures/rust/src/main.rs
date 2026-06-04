fn urban_viability(infrastructure: f64, governance: f64, housing: f64, climate: f64, inequality: f64, digital: f64, finance: f64, cohesion: f64, maintenance: f64) -> f64 {
    0.17 * infrastructure + 0.16 * governance + 0.14 * housing - 0.14 * climate
        - 0.14 * inequality + 0.09 * digital + 0.12 * finance + 0.14 * cohesion
        - 0.08 * maintenance
}

fn main() {
    let score = urban_viability(0.78, 0.78, 0.74, 0.42, 0.40, 0.68, 0.76, 0.74, 0.34);
    println!("Adaptive Public City viability={:.4}", score);
}
