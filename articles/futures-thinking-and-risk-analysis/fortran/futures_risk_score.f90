program futures_risk_score
  implicit none
  real :: score

  score = 0.12*(1.0-0.18) + 0.16*0.88 + 0.14*0.91 + 0.15*0.84 - &
          0.11*0.31 - 0.10*0.28 - 0.08*0.26 + 0.12*0.94 + &
          0.10*0.92 - 0.02*0.30

  print *, "Systemic Cascade futures risk score:", score
end program futures_risk_score
