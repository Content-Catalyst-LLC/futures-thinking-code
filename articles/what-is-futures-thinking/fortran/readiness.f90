program readiness
  implicit none
  real :: values(6)
  real :: avg, worst, best, volatility, robustness

  values = (/0.78, 0.75, 0.72, 0.70, 0.73, 0.69/)
  avg = sum(values) / size(values)
  worst = minval(values)
  best = maxval(values)
  volatility = sqrt(sum((values - avg)**2) / size(values))
  robustness = 0.45 * worst + 0.35 * avg - 0.20 * volatility

  print *, "Flexible Foresight Strategy robustness:", robustness
end program readiness
