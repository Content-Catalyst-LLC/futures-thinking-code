# Julia standard-library example for infrastructure viability scoring.

profiles = Dict(
    "Adaptive Public Infrastructure" => [0.46, 0.78, 0.58, 0.42, 0.78, 0.76, 0.80, 0.76, 0.38],
    "Climate-Stressed Legacy Network" => [0.71, 0.29, 0.57, 0.88, 0.41, 0.36, 0.30, 0.38, 0.58],
    "Distributed Resilience Model" => [0.35, 0.82, 0.48, 0.46, 0.69, 0.62, 0.70, 0.68, 0.40]
)

function infrastructure_viability(v)
    # v = centralization redundancy digital climate coordination finance maintenance equity geopolitics
    0.14*(1-v[1]) + 0.18*v[2] - 0.12*v[3] - 0.16*v[4] + 0.16*v[5] +
    0.12*v[6] + 0.12*v[7] + 0.10*v[8] - 0.08*v[9]
end

println("profile,infrastructure_viability")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(infrastructure_viability(values), digits=4))")
end
