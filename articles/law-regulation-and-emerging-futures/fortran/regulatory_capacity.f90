program regulatory_capacity
  implicit none
  real :: score

  score = 0.13*0.70 + 0.12*0.76 + 0.12*0.78 + 0.14*0.90 + 0.10*0.62 + &
          0.12*0.72 + 0.10*0.74 + 0.08*0.72 + 0.05*0.66 + 0.04*0.86

  print *, "Rights-Centered Technology Regulation capacity:", score
end program regulatory_capacity
