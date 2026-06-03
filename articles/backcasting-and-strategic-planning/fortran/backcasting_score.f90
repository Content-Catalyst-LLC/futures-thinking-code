program backcasting_score
  implicit none
  real :: v(8)
  real :: score

  v = (/0.66, 0.56, 0.52, 0.78, 0.72, 0.86, 0.80, 0.40/)
  score = 0.18*v(1) - 0.16*v(2) + 0.14*v(3) + 0.18*v(4) + 0.16*v(5) + 0.12*v(6) + 0.14*v(7) - 0.12*v(8)

  print *, "Public Accountability Before Scale viability:", score
end program backcasting_score
