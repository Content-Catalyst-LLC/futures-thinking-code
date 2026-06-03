fn reflective_score(methodological: f64, participation: f64, ethics: f64, systems: f64) -> f64 {
    0.25 * methodological + 0.25 * participation + 0.25 * ethics + 0.25 * systems
}

fn power_risk(institutional_power: f64, participation: f64, ethics: f64) -> f64 {
    institutional_power * (1.0 - participation) * (1.0 - ethics)
}

fn main() {
    let score = reflective_score(0.68, 0.92, 0.86, 0.64);
    let risk = power_risk(0.42, 0.92, 0.86);
    println!(
        "Participatory and Democratic Futures: reflective_score={:.4}, power_risk={:.4}",
        score, risk
    );
}
