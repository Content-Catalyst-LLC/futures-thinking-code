program supply_chain_resilience
  implicit none
  real :: score

  score = 0.10*0.52 + 0.16*0.76 + 0.14*0.84 + 0.14*0.74 + 0.12*0.72 + &
          0.13*0.70 + 0.09*0.76 + 0.06*0.54 + 0.04*0.80 + 0.02*0.86

  print *, "Essential Goods Resilience Model resilience:", score
end program supply_chain_resilience
