program infrastructure_viability
  implicit none
  real :: score

  score = 0.14*(1.0-0.46) + 0.18*0.78 - 0.12*0.58 - 0.16*0.42 + 0.16*0.78 + &
          0.12*0.76 + 0.12*0.80 + 0.10*0.76 - 0.08*0.38

  print *, "Adaptive Public Infrastructure viability:", score
end program infrastructure_viability
