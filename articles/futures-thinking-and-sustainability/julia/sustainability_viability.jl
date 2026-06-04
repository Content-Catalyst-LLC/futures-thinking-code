# Julia standard-library example for sustainability viability scoring.

profiles = Dict(
    "Managed Sustainable Transition" => [0.78, 0.72, 0.79, 0.66, 0.76, 0.72, 0.78, 0.74, 0.34],
    "High-Consumption Fragile Future" => [0.32, 0.38, 0.46, 0.42, 0.29, 0.42, 0.40, 0.34, 0.84],
    "Just Transformative Sustainability" => [0.82, 0.82, 0.80, 0.70, 0.78, 0.76, 0.82, 0.86, 0.30]
)

function sustainability_viability(v)
    # v = ecology equity adaptive technology governance finance resilience justice degradation
    0.17*v[1] + 0.15*v[2] + 0.14*v[3] + 0.10*v[4] + 0.14*v[5] +
    0.10*v[6] + 0.10*v[7] + 0.10*v[8] - 0.08*v[9]
end

println("profile,sustainability_viability")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(sustainability_viability(values), digits=4))")
end
