program horizon_signal_score
  implicit none
  real :: v(7)
  real :: score

  v = (/0.48, 0.57, 0.90, 0.82, 0.72, 0.84, 0.91/)
  score = 0.10*v(1) - 0.08*v(2) + 0.22*v(3) + 0.18*v(4) + 0.14*v(5) + 0.14*v(6) + 0.30*v(7)

  print *, "Climate insurance withdrawal signal profile:", score
end program horizon_signal_score
