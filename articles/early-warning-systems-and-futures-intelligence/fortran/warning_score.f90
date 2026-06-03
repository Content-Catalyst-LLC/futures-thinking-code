program warning_score_example
  implicit none
  real :: v(7)
  real :: score

  v = (/0.58, 0.90, 0.88, 0.82, 0.68, 0.92, 0.80/)
  score = 0.12*v(1) + 0.22*v(2) + 0.20*v(3) + 0.13*v(4) + &
          0.11*v(5) + 0.13*v(6) + 0.09*v(7)

  print *, "Rising heat-health emergency demand warning score:", score
end program warning_score_example
