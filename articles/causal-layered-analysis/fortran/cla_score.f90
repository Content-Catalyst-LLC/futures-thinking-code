program cla_score
  implicit none
  real :: v(7)
  real :: score

  v = (/0.90, 0.88, 0.84, 0.86, 0.88, 0.94, 0.92/)
  score = 0.10*v(1) + 0.18*v(2) + 0.22*v(3) + 0.20*v(4) + 0.16*v(5) + 0.08*v(6) + 0.06*v(7)

  print *, "Climate adaptation and housing CLA depth:", score
end program cla_score
