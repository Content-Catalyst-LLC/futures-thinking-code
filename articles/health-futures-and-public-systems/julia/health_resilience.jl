# Julia standard-library example for health futures resilience scoring.

profiles = Dict(
    "Preventive Public Health Renewal" => [0.82, 0.74, 0.86, 0.70, 0.72, 0.66, 0.78, 0.76, 0.80, 0.72],
    "High-Tech Fragmented Medicine" => [0.46, 0.58, 0.48, 0.42, 0.44, 0.34, 0.42, 0.38, 0.34, 0.40],
    "Equitable Health Systems Transformation" => [0.86, 0.84, 0.88, 0.78, 0.76, 0.78, 0.84, 0.82, 0.88, 0.80]
)

function health_resilience(v)
    # v = prevention access public_health climate workforce tech social trust equity care
    0.13*v[1] + 0.12*v[2] + 0.15*v[3] + 0.10*v[4] + 0.11*v[5] +
    0.08*v[6] + 0.11*v[7] + 0.08*v[8] + 0.07*v[9] + 0.05*v[10]
end

println("profile,public_health_resilience")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(health_resilience(values), digits=4))")
end
