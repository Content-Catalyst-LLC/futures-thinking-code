program inherited_burden_score
  implicit none
  real :: score

  score = 0.18*0.88 + 0.14*0.76 + 0.16*0.70 + 0.18*0.84 + 0.14*0.62 + &
          0.10*(1.0-0.38) + 0.06*(1.0-0.36) + 0.04*(1.0-0.24)

  print *, "Short-Term Extraction inherited burden:", score
end program inherited_burden_score
