program transformation_capacity
  implicit none
  real :: score

  score = 0.22*0.78 + 0.22*0.86 + 0.20*0.82 + 0.18*0.74 + &
          0.10*(1.0 - 0.44) + 0.08*0.68

  print *, "Justice-centered public transformation capacity:", score
end program transformation_capacity
