program futures_wheel_score
  implicit none
  real :: v(5)
  real :: score

  v = (/0.84, 0.90, 0.36, 0.94, 0.78/)
  score = 0.22*v(1) + 0.26*v(2) + 0.14*v(3) + 0.22*v(4) + 0.16*v(5)

  print *, "Heat-related health emergencies consequence priority:", score
end program futures_wheel_score
