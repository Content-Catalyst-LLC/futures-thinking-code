# Julia standard-library example for economic development quality scoring.

futures = Dict(
    "High-Growth Unequal Future" => [0.82, 0.78, 0.74, 0.48, 0.44, 0.50, 0.42, 0.46, 0.70, 0.50, 0.44],
    "Green Coordinated Transition" => [0.64, 0.42, 0.36, 0.76, 0.79, 0.68, 0.70, 0.78, 0.68, 0.72, 0.70],
    "Human Capability Renaissance" => [0.58, 0.36, 0.40, 0.82, 0.78, 0.72, 0.80, 0.84, 0.62, 0.66, 0.82]
)

function development_quality(v)
    # v = growth, inequality, ecology, institutions, resilience, fiscal, labor, public investment, tech, trade, legitimacy
    0.14*v[1] - 0.12*v[2] - 0.14*v[3] + 0.13*v[4] + 0.12*v[5] +
    0.08*v[6] + 0.08*v[7] + 0.08*v[8] + 0.06*v[9] + 0.03*v[10] + 0.02*v[11]
end

println("future,development_quality")
for (name, values) in sort(collect(futures))
    println("$(name),$(round(development_quality(values), digits=4))")
end
