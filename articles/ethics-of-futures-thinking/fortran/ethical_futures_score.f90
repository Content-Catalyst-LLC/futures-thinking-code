program ethical_futures_score
  implicit none
  real :: score

  score = 0.13*0.72 + 0.12*0.84 + 0.12*0.76 + 0.12*0.82 + 0.10*0.78 + &
          0.10*0.80 + 0.10*0.74 + 0.08*0.72 + 0.08*0.86 + 0.05*0.82

  print *, "Civil Society Coalition ethical futures profile:", score
end program ethical_futures_score
