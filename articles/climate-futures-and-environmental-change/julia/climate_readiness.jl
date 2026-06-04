# Julia standard-library example for climate readiness scoring.

profiles = Dict(
    "Managed Low-Carbon Transition" => [0.32, 0.72, 0.36, 0.74, 0.42, 0.66, 0.71, 0.68, 0.34],
    "Delayed Transition High Stress" => [0.84, 0.38, 0.81, 0.34, 0.72, 0.42, 0.27, 0.34, 0.76],
    "Just Climate Transformation" => [0.26, 0.78, 0.34, 0.78, 0.34, 0.70, 0.76, 0.82, 0.28]
)

function climate_readiness(v)
    # v = emissions adaptation ecosystem governance vulnerability technology transition justice residual_loss
    -0.16*v[1] + 0.15*v[2] - 0.15*v[3] + 0.14*v[4] - 0.12*v[5] +
    0.10*v[6] + 0.14*v[7] + 0.12*v[8] - 0.10*v[9]
end

println("profile,climate_readiness")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(climate_readiness(values), digits=4))")
end
