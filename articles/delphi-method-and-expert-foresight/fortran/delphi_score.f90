program delphi_score
  implicit none
  real :: v(4)
  real :: score

  v = (/0.69, 0.92, 0.87, 0.61/)
  score = 0.25*v(1) + 0.35*v(2) + 0.25*v(3) + 0.15*v(4)

  print *, "Public AI accountability Delphi judgment profile:", score
end program delphi_score
