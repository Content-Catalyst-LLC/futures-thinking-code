program trend_profile_score
  implicit none
  real :: v(6)
  real :: score

  v = (/0.74, 0.86, 0.88, 0.22, 0.52, 0.86/)
  score = 0.20*v(1) + 0.22*v(2) + 0.22*v(3) - 0.12*v(4) - 0.14*v(5) + 0.10*v(6)

  print *, "Climate Risk Intensification profile:", score
end program trend_profile_score
