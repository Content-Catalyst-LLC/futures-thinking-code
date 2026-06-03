fn transition_readiness(clean: f64, grid: f64, storage: f64, electrification: f64, phase_down: f64, justice: f64, labor: f64, materials: f64, resilience: f64) -> f64 {
    0.14 * clean + 0.14 * grid + 0.12 * storage + 0.12 * electrification
        + 0.12 * phase_down + 0.12 * justice + 0.10 * labor + 0.08 * materials + 0.06 * resilience
}

fn main() {
    let score = transition_readiness(0.82, 0.78, 0.74, 0.76, 0.78, 0.84, 0.82, 0.76, 0.80);
    println!("Managed Just Transition readiness={:.4}", score);
}
