program future_category_score
  implicit none
  real :: v(8)
  real :: plausibility, probability, preference, priority

  v = (/0.62, 0.70, 0.56, 0.42, 0.86, 0.78, 0.84, 0.90/)

  plausibility = 0.40*v(1) + 0.35*v(2) + 0.25*v(3)
  probability = 0.70*v(4) + 0.30*v(1)
  preference = 0.30*v(5) + 0.25*v(6) + 0.25*v(7) + 0.20*v(8)
  priority = 0.35*plausibility + 0.25*probability + 0.40*preference

  print *, "Participatory Anticipatory Governance priority:", priority
end program future_category_score
