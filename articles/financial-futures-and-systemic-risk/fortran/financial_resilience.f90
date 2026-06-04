program financial_resilience
  implicit none
  real :: score

  score = 0.14*0.82 + 0.14*0.80 + 0.14*0.86 + 0.10*0.78 + 0.10*0.84 + &
          0.10*0.76 + 0.10*(1.0-0.42) + 0.08*(1.0-0.44) + 0.06*(1.0-0.48) + 0.04*(1.0-0.38)

  print *, "Resilient Public-Interest Finance resilience:", score
end program financial_resilience
