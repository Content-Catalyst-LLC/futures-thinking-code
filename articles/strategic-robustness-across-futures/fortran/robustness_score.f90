program robustness_score
  implicit none
  real :: values(4)
  real :: worst_case

  values = (/0.66, 0.72, 0.78, 0.70/)
  worst_case = minval(values)

  print *, "Robust resilience portfolio worst-case viability:", worst_case
end program robustness_score
