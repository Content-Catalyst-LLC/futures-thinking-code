program scenario_score
  implicit none
  real :: v(4)
  real :: score

  v = (/1.55, 1.02, 1.28, 0.15/)
  score = 0.35*v(1) + 0.30*v(2) + 0.20*v(3) + 0.15*v(4)

  print *, "Robust resilience portfolio viability:", score
end program scenario_score
