program biotechnology_capacity
  implicit none
  real :: score

  score = 0.16*0.68 + 0.18*0.82 + 0.16*0.84 + 0.16*0.86 + &
          0.12*0.62 + 0.12*0.88 + 0.05*(1.0 - 0.46) + 0.05*(1.0 - 0.34)

  print *, "Democratic Biofutures responsible biotechnology capacity:", score
end program biotechnology_capacity
