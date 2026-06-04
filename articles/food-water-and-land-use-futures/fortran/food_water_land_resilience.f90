program food_water_land_resilience
  implicit none
  real :: score

  score = 0.13*0.72 + 0.16*0.76 + 0.15*0.82 + 0.14*0.78 + 0.14*0.76 - &
          0.12*0.42 - 0.08*0.38 + 0.14*0.80 + 0.12*0.78

  print *, "Regenerative Transition resilience:", score
end program food_water_land_resilience
