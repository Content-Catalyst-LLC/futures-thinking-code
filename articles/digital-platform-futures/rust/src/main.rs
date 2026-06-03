fn public_interest_capacity(platform_power: f64, data_advantage: f64, interoperability: f64, worker_protection: f64, public_accountability: f64, user_rights: f64, ecological_responsibility: f64, digital_public_value: f64) -> f64 {
    0.18 * interoperability + 0.18 * public_accountability + 0.16 * user_rights
        + 0.14 * worker_protection + 0.14 * digital_public_value + 0.10 * ecological_responsibility
        + 0.05 * (1.0 - platform_power) + 0.05 * (1.0 - data_advantage)
}

fn main() {
    let score = public_interest_capacity(0.42, 0.46, 0.76, 0.70, 0.82, 0.84, 0.70, 0.86);
    println!("Digital Public Infrastructure Turn public-interest platform capacity={:.4}", score);
}
