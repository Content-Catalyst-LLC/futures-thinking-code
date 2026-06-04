program disciplined_hope_score
  implicit none
  real :: score

  score = 0.18*0.86 + 0.18*0.84 + 0.16*0.76 + 0.16*0.80 + &
          0.14*0.88 + 0.12*0.92 - 0.04*0.28 - 0.02*0.30

  print *, "Reparative Imagination disciplined hope:", score
end program disciplined_hope_score
