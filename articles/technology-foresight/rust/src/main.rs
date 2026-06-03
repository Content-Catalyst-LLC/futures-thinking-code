fn enabling_score(m: f64, c: f64, s: f64, i: f64, g: f64, l: f64, e: f64) -> f64 { 0.16*m + 0.18*c + 0.16*s + 0.16*i + 0.14*g + 0.12*l + 0.08*(1.0-e) }
fn main() { println!("Renewable energy acceleration enabling score={:.4}", enabling_score(0.78,0.74,0.74,0.68,0.66,0.72,0.48)); }
