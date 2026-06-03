program consumer_future_health
  implicit none
  real :: score

  score = 0.14*0.70 + 0.16*0.76 + 0.10*0.70 + 0.16*0.86 + 0.10*(1.0-0.70) + &
          0.12*(1.0-0.42) + 0.06*0.66 + 0.06*0.68 + 0.06*0.70 + 0.04*0.76

  print *, "Access and Inclusion Market health:", score
end program consumer_future_health
