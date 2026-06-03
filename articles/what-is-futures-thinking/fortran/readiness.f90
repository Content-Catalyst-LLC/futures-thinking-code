program readiness
  implicit none
  real :: values(5)
  real :: avg, worst, volatility, robustness
  real :: adaptability, equity, difficulty

  values = (/0.78, 0.76, 0.74, 0.71, 0.79/)
  adaptability = 0.84
  equity = 0.72
  difficulty = 0.58

  avg = sum(values) / size(values)
  worst = minval(values)
  volatility = sqrt(sum((values - avg)**2) / size(values))
  robustness = 0.45 * worst + 0.30 * avg + 0.15 * adaptability + 0.10 * equity - 0.15 * volatility - 0.05 * difficulty

  print *, "Flexible Foresight Strategy robustness:", robustness
end program readiness
