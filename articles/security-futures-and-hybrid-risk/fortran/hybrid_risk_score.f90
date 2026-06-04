program hybrid_risk_score
  implicit none
  real :: score

  score = 0.13*0.88 + 0.13*0.92 + 0.13*0.90 + 0.12*0.88 + 0.10*0.84 + &
          0.11*(1.0-0.22) + 0.10*(1.0-0.20) + 0.10*(1.0-0.18) + &
          0.05*(1.0-0.16) + 0.03*(1.0-0.22)

  print *, "Systemic Security Breakdown hybrid risk:", score
end program hybrid_risk_score
