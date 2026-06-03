program anticipatory_capacity
  implicit none
  real :: score

  score = 0.12*0.68 + 0.12*0.74 + 0.12*0.78 + 0.12*0.70 + 0.12*0.86 + &
          0.10*0.72 + 0.10*0.68 + 0.08*0.88 + 0.07*0.78 + 0.05*0.64

  print *, "Participatory Anticipatory Governance capacity:", score
end program anticipatory_capacity
