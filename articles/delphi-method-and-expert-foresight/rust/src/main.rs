fn judgment_profile(v: &[f64]) -> f64 {
    0.25 * v[0] + 0.35 * v[1] + 0.25 * v[2] + 0.15 * v[3]
}

fn main() {
    let public_ai_accountability = [0.69, 0.92, 0.87, 0.61];
    println!(
        "Public AI accountability Delphi judgment profile={:.4}",
        judgment_profile(&public_ai_accountability)
    );
}
