program adaptive_profile
  implicit none
  real :: score

  score = 0.18*0.72 + 0.16*0.68 + 0.16*0.66 + 0.14*0.86 + &
          0.14*0.76 + 0.10*0.54 + 0.08*0.70 - 0.10*0.40 + 0.04*0.82

  print *, "Participatory Governance Assembly adaptive profile:", score
end program adaptive_profile
