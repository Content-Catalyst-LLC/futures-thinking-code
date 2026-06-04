program coloniality_risk_score
  implicit none
  real :: score

  score = 0.12*0.86 + 0.12*(1.0-0.34) + 0.12*0.90 + 0.12*0.82 + &
          0.11*(1.0-0.36) + 0.10*(1.0-0.38) + 0.10*0.78 + &
          0.09*(1.0-0.24) + 0.07*(1.0-0.30) + 0.03*(1.0-0.28) + &
          0.02*(1.0-0.44)

  print *, "Green Extraction Continuity coloniality risk:", score
end program coloniality_risk_score
