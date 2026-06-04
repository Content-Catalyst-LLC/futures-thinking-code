program health_resilience
  implicit none
  real :: score

  score = 0.13*0.86 + 0.12*0.84 + 0.15*0.88 + 0.10*0.78 + 0.11*0.76 + &
          0.08*0.78 + 0.11*0.84 + 0.08*0.82 + 0.07*0.88 + 0.05*0.80

  print *, "Equitable Health Systems Transformation resilience:", score
end program health_resilience
