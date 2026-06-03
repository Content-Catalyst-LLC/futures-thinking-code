program democratic_capacity
  implicit none
  real :: score

  score = 0.11*0.82 + 0.12*0.78 + 0.11*0.80 + 0.14*0.78 + 0.12*0.82 + &
          0.12*0.84 + 0.08*0.78 + 0.10*0.80 + 0.05*0.76 + 0.05*0.86

  print *, "Co-Governance Futures Board capacity:", score
end program democratic_capacity
