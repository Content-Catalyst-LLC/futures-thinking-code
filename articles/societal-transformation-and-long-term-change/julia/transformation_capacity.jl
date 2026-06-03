# Julia standard-library example for just-transformation capacity.

scenarios = Dict(
    "Fragmented Disruptive Transition" => [0.36, 0.28, 0.30, 0.31, 0.68, 0.72],
    "Coordinated Adaptive Transformation" => [0.81, 0.70, 0.76, 0.78, 0.39, 0.61],
    "Justice-Centered Public Transformation" => [0.78, 0.86, 0.82, 0.74, 0.44, 0.68]
)

function just_capacity(v)
    # v = institution, equity, legitimacy, cohesion, ecology, economy
    0.22*v[1] + 0.22*v[2] + 0.20*v[3] + 0.18*v[4] + 0.10*(1 - v[5]) + 0.08*v[6]
end

println("scenario,just_transformation_capacity")
for (name, values) in sort(collect(scenarios))
    println("$(name),$(round(just_capacity(values), digits=4))")
end
