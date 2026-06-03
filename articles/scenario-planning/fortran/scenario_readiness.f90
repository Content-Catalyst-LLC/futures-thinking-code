program scenario_readiness
  implicit none
  real :: values(5)
  real :: avg, worst, volatility, score

  values = (/0.74, 0.76, 0.73, 0.70, 0.80/)
  avg = sum(values) / size(values)
  worst = minval(values)
  volatility = sqrt(sum((values - avg)**2) / size(values))
  score = 0.55 * worst + 0.35 * avg - 0.10 * volatility

  print *, "Robust Adaptive Strategy robustness:", score
end program scenario_readiness
