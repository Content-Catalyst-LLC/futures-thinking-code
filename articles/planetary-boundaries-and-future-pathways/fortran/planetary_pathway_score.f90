program planetary_pathway_score
  implicit none
  real :: pressure, score

  pressure = 0.16*0.32 + 0.16*0.30 + 0.12*0.34 + 0.12*0.30 + 0.10*0.32 + &
             0.10*0.34 + 0.08*0.30 + 0.10*0.36 + 0.06*0.56

  score = 0.22*0.82 + 0.20*0.80 + 0.20*0.84 + 0.14*0.78 - 0.20*pressure + 0.04*(1.0-0.56)

  print *, "Safe and Just Transformation boundary pressure:", pressure
  print *, "Safe and Just Transformation safe-and-just score:", score
end program planetary_pathway_score
