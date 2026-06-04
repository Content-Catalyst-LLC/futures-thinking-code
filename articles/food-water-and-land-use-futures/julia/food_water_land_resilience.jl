# Julia standard-library example for food-water-land resilience scoring.

profiles = Dict(
    "Regenerative Transition" => [0.72, 0.76, 0.82, 0.78, 0.76, 0.42, 0.38, 0.80, 0.78],
    "High-Yield Degradation" => [0.86, 0.44, 0.32, 0.30, 0.50, 0.58, 0.62, 0.42, 0.46],
    "Watershed Restoration" => [0.68, 0.82, 0.78, 0.84, 0.72, 0.46, 0.44, 0.76, 0.80]
)

function fwl_resilience(v)
    # v = production water soil biodiversity governance climate market justice livelihoods
    0.13*v[1] + 0.16*v[2] + 0.15*v[3] + 0.14*v[4] + 0.14*v[5] -
    0.12*v[6] - 0.08*v[7] + 0.14*v[8] + 0.12*v[9]
end

println("profile,food_water_land_resilience")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(fwl_resilience(values), digits=4))")
end
