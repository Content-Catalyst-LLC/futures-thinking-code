fn data_quality(completeness: f64, validity: f64, freshness: f64, traceability: f64) -> f64 { 0.25*completeness + 0.25*validity + 0.25*freshness + 0.25*traceability }
fn main() { println!("Public trust driver data quality={:.4}", data_quality(1.0,0.95,0.78,0.70)); }
