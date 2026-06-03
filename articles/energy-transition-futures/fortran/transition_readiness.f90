program transition_readiness
  implicit none
  real :: score

  score = 0.14*0.82 + 0.14*0.78 + 0.12*0.74 + 0.12*0.76 + &
          0.12*0.78 + 0.12*0.84 + 0.10*0.82 + 0.08*0.76 + 0.06*0.80

  print *, "Managed Just Transition readiness:", score
end program transition_readiness
