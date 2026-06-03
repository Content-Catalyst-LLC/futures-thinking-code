program systems_foresight_score
  implicit none
  real :: v(5)
  real :: score

  v = (/0.86, 0.46, 0.52, 0.88, 0.90/)
  score = 0.26*v(1) + 0.22*(1.0-v(2)) + 0.18*(1.0-v(3)) + 0.18*v(4) + 0.16*v(5)

  print *, "Climate adaptation structural pressure:", score
end program systems_foresight_score
