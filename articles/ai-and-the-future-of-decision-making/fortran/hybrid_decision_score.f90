program hybrid_decision_score
  implicit none
  real :: score

  score = 0.16*0.72 + 0.16*0.74 + 0.16*0.83 + 0.12*0.79 + &
          0.12*0.78 + 0.12*0.82 + 0.08*0.80 + 0.08*0.76

  print *, "High-governance hybrid decision profile:", score
end program hybrid_decision_score
