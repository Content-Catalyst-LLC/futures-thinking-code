program climate_readiness
  implicit none
  real :: score

  score = -0.16*0.26 + 0.15*0.78 - 0.15*0.34 + 0.14*0.78 - 0.12*0.34 + &
          0.10*0.70 + 0.14*0.76 + 0.12*0.82 - 0.10*0.28

  print *, "Just Climate Transformation readiness:", score
end program climate_readiness
