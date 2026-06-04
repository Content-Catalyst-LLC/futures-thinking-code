program demographic_stress_score
  implicit none
  real :: score

  score = 0.13*0.62 + 0.13*0.70 + 0.12*0.80 + 0.13*(1.0-0.34) + 0.12*0.74 + &
          0.10*(1.0-0.36) + 0.11*0.62 + 0.08*(1.0-0.22) + &
          0.05*(1.0-0.28) + 0.03*(1.0-0.38)

  print *, "Demographic Fear Politics stress:", score
end program demographic_stress_score
