program weak_signal_score
  implicit none
  real :: v(7)
  real :: score

  v = (/0.48, 0.57, 0.90, 0.82, 0.55, 0.86, 0.88/)
  score = 0.10*v(1) - 0.08*v(2) + 0.24*v(3) + 0.22*v(4) + 0.12*v(5) + 0.12*v(6) + 0.20*v(7)

  print *, "Climate insurance withdrawal weak signal profile:", score
end program weak_signal_score
