fn regulatory_capacity(foresight: f64, monitoring: f64, enforcement: f64, rights: f64, participation: f64, revision: f64, learning: f64, capture: f64, certainty: f64, remedy: f64) -> f64 {
    0.13 * foresight + 0.12 * monitoring + 0.12 * enforcement + 0.14 * rights
        + 0.10 * participation + 0.12 * revision + 0.10 * learning + 0.08 * capture
        + 0.05 * certainty + 0.04 * remedy
}

fn main() {
    let score = regulatory_capacity(0.70, 0.76, 0.78, 0.90, 0.62, 0.72, 0.74, 0.72, 0.66, 0.86);
    println!("Rights-Centered Technology Regulation capacity={:.4}", score);
}
