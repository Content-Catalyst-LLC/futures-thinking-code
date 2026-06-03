program readiness_score
  implicit none
  real :: score
  score = 0.16*0.78 + 0.18*0.74 + 0.16*0.74 + 0.16*0.68 + 0.14*0.66 + 0.12*0.72 + 0.08*(1.0 - 0.48)
  print *, "Renewable energy acceleration enabling score:", score
end program readiness_score
