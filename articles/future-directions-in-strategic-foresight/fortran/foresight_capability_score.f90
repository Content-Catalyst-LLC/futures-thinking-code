program foresight_capability_score
  implicit none
  real :: score

  score = 0.16*0.76 + 0.16*0.74 + 0.14*0.72 + 0.14*0.70 + &
          0.12*0.66 + 0.10*0.66 + 0.10*0.72 + 0.08*0.68

  print *, "Climate Adaptation Authority foresight capability:", score
end program foresight_capability_score
