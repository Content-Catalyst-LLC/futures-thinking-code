program history_score
  implicit none
  real :: methodological, participation, ethics, systems, institutional_power
  real :: reflective_score, power_risk

  methodological = 0.68
  participation = 0.92
  ethics = 0.86
  systems = 0.64
  institutional_power = 0.42

  reflective_score = 0.25*methodological + 0.25*participation + 0.25*ethics + 0.25*systems
  power_risk = institutional_power * (1 - participation) * (1 - ethics)

  print *, "Participatory and Democratic Futures reflective score:", reflective_score
  print *, "Participatory and Democratic Futures power risk:", power_risk
end program history_score
