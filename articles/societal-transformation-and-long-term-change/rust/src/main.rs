fn just_capacity(institution: f64, equity: f64, legitimacy: f64, cohesion: f64, ecology: f64, economy: f64) -> f64 {
    0.22 * institution + 0.22 * equity + 0.20 * legitimacy + 0.18 * cohesion + 0.10 * (1.0 - ecology) + 0.08 * economy
}

fn main() {
    let score = just_capacity(0.78, 0.86, 0.82, 0.74, 0.44, 0.68);
    println!("Justice-centered public transformation capacity={:.4}", score);
}
