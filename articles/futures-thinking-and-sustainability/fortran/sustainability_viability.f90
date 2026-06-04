program sustainability_viability
  implicit none
  real :: score

  score = 0.17*0.82 + 0.15*0.82 + 0.14*0.80 + 0.10*0.70 + 0.14*0.78 + &
          0.10*0.76 + 0.10*0.82 + 0.10*0.86 - 0.08*0.30

  print *, "Just Transformative Sustainability viability:", score
end program sustainability_viability
