program foresight_method_score
  implicit none
  real :: values(7)
  real :: weights(7)
  real :: score

  values = (/0.42, 0.82, 0.84, 0.72, 0.62, 0.76, 0.86/)
  weights = (/0.16, 0.14, 0.16, 0.18, 0.14, 0.10, 0.12/)
  score = sum(values * weights)

  print *, "Scenario Planning foresight method profile:", score
end program foresight_method_score
