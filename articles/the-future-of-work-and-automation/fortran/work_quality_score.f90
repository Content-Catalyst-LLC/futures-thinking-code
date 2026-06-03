program work_quality_score
  implicit none
  real :: score

  score = 0.28*0.70 + 0.18*0.66 + 0.18*0.54 + 0.16*0.60 + &
          0.12*0.72 + 0.08*(1.0 - 0.46)

  print *, "Knowledge work adjusted job quality:", score
end program work_quality_score
