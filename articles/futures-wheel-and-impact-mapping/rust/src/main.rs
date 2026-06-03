fn consequence_priority(v: &[f64]) -> f64 {
    0.22 * v[0] + 0.26 * v[1] + 0.14 * v[2] + 0.22 * v[3] + 0.16 * v[4]
}

fn main() {
    let heat_health = [0.84, 0.90, 0.36, 0.94, 0.78];
    println!(
        "Heat-related health emergencies consequence priority={:.4}",
        consequence_priority(&heat_health)
    );
}
