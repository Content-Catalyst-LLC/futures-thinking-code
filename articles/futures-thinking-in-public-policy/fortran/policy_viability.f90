program policy_viability
  implicit none
  real :: score

  score = 0.20*0.80 + 0.16*0.84 + 0.18*0.82 + 0.14*0.76 + &
          0.14*0.86 + 0.08*0.56 + 0.06*0.82 + 0.04*0.84

  print *, "Participatory Anticipatory Policy futures profile:", score
end program policy_viability
