program geopolitical_stability
  implicit none
  real :: score
  score = 0.11*(1.0-0.44) + 0.10*0.70 + 0.16*0.82 - 0.12*0.46 - 0.12*0.48 - 0.11*0.38 + 0.12*0.74 + 0.11*0.70 + 0.08*0.72 + 0.07*0.78
  print *, "Institutional Renewal geopolitical stability:", score
end program geopolitical_stability
