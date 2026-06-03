program data_quality_score
  implicit none
  real :: score
  score = 0.25*1.00 + 0.25*0.95 + 0.25*0.78 + 0.25*0.70
  print *, "Public trust driver data quality:", score
end program data_quality_score
