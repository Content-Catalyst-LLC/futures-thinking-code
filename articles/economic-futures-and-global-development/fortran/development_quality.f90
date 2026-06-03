program development_quality
  implicit none
  real :: score

  score = 0.14*0.64 - 0.12*0.42 - 0.14*0.36 + 0.13*0.76 + 0.12*0.79 + &
          0.08*0.68 + 0.08*0.70 + 0.08*0.78 + 0.06*0.68 + 0.03*0.72 + 0.02*0.70

  print *, "Green Coordinated Transition development_quality:", score
end program development_quality
