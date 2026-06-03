program readiness
  implicit none
  real :: values(6)
  real :: avg, worst, best, volatility, robustness
  integer :: i

  values = (/0.78, 0.75, 0.72, 0.70, 0.73, 0.69/)
  avg = sum(values) / size(values)
  worst = minval(values)
  best = maxval(values)
  volatility = sqrt(sum((values - avg)**2) / size(values))
  robustness = 0.45 * worst + 0.35 * avg - 0.20 * volatility

  print *, "Flexible Foresight Strategy"
  print *, "Mean performance:", avg
  print *, "Worst case:", worst
  print *, "Best case:", best
  print *, "Volatility:", volatility
  print *, "Robustness:", robustness
end program readiness
