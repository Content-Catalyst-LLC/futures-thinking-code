program driver_priority_score
  implicit none
  real :: v(8)
  real :: score

  v = (/0.88, 0.82, 0.80, 0.84, 0.84, 0.70, 0.68, 0.54/)
  score = 0.22*v(1) + 0.20*v(2) + 0.14*v(3) + 0.14*v(4) + &
          0.12*v(5) + 0.08*v(6) + 0.06*v(7) + 0.04*(1.0-v(8))

  print *, "Public trust driver priority:", score
end program driver_priority_score
