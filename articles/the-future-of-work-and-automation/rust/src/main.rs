fn job_quality(wage_security: f64, worker_voice: f64, training: f64, protection: f64, surveillance: f64, initial_quality: f64) -> f64 {
    0.28 * initial_quality + 0.18 * wage_security + 0.18 * worker_voice
        + 0.16 * protection + 0.12 * training + 0.08 * (1.0 - surveillance)
}

fn main() {
    let score = job_quality(0.66, 0.54, 0.72, 0.60, 0.46, 0.70);
    println!("Knowledge work adjusted job quality={:.4}", score);
}
