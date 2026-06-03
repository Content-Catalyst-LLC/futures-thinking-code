function enabling_score(maturity, capability, support, infrastructure, governance, legitimacy, ecological_pressure)
    0.16*maturity + 0.18*capability + 0.16*support + 0.16*infrastructure + 0.14*governance + 0.12*legitimacy + 0.08*(1 - ecological_pressure)
end
println("technology,enabling_score")
println("Renewable Energy Acceleration,$(round(enabling_score(0.78,0.74,0.74,0.68,0.66,0.72,0.48), digits=4))")
