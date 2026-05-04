program scenario_readiness
  implicit none

  real, dimension(6) :: values
  real :: mean_value, worst, best, range_value, score

  values = (/0.72, 0.78, 0.74, 0.73, 0.69, 0.80/)

  mean_value = sum(values) / size(values)
  worst = minval(values)
  best = maxval(values)
  range_value = best - worst

  score = 0.50 * worst + 0.30 * mean_value - 0.20 * range_value

  print *, "Scenario robustness score:", score

end program scenario_readiness
