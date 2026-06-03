program foresight_capacity
  implicit none
  real :: score

  score = 0.12*0.68 + 0.12*0.78 + 0.14*0.68 + 0.12*0.90 + 0.12*0.62 + &
          0.10*0.76 + 0.10*0.80 + 0.10*0.60 + 0.05*0.72 + 0.03*0.86

  print *, "Participatory Public Foresight System capacity:", score
end program foresight_capacity
