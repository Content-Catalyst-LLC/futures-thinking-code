fn worst_case_viability(values: &[f64]) -> f64 {
    values
        .iter()
        .copied()
        .fold(f64::INFINITY, f64::min)
}

fn main() {
    let robust_resilience = [0.66, 0.72, 0.78, 0.70];
    println!(
        "Robust resilience portfolio worst-case viability={:.4}",
        worst_case_viability(&robust_resilience)
    );
}
