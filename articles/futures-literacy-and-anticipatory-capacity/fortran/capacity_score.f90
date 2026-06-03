program capacity_score
  implicit none
  real :: values(7)
  real :: weights(7)
  real :: score

  values = (/0.82, 0.84, 0.88, 0.90, 0.72, 0.84, 0.80/)
  weights = (/0.15, 0.15, 0.17, 0.13, 0.17, 0.13, 0.10/)
  score = sum(values * weights)

  print *, "Futures-Literate Organization anticipatory capacity:", score
end program capacity_score
