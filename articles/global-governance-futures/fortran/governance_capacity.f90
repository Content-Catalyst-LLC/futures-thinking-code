program governance_capacity
  implicit none
  real :: score

  score = 0.14*0.82 + 0.16*0.88 + 0.12*0.78 + 0.11*0.80 + 0.13*0.84 + &
          0.10*0.78 + 0.10*0.86 + 0.08*0.88 + 0.08*0.90 + 0.08*0.92

  print *, "Democratic Justice Governance capacity:", score
end program governance_capacity
