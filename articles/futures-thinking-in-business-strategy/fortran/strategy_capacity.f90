program strategy_capacity
  implicit none
  real :: score

  score = 0.14*0.82 - 0.10*0.52 + 0.15*0.72 + 0.14*0.79 + 0.10*0.68 + &
          0.12*0.80 + 0.08*0.66 + 0.09*0.70 + 0.08*0.76

  print *, "Adaptive Innovation Strategy readiness:", score
end program strategy_capacity
