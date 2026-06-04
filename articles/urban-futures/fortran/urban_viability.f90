program urban_viability
  implicit none
  real :: score

  score = 0.17*0.78 + 0.16*0.78 + 0.14*0.74 - 0.14*0.42 - 0.14*0.40 + &
          0.09*0.68 + 0.12*0.76 + 0.14*0.74 - 0.08*0.34

  print *, "Adaptive Public City viability:", score
end program urban_viability
