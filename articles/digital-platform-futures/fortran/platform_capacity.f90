program platform_capacity
  implicit none
  real :: score

  score = 0.18*0.76 + 0.18*0.82 + 0.16*0.84 + 0.14*0.70 + &
          0.14*0.86 + 0.10*0.70 + 0.05*(1.0 - 0.42) + 0.05*(1.0 - 0.46)

  print *, "Digital Public Infrastructure Turn public-interest platform capacity:", score
end program platform_capacity
