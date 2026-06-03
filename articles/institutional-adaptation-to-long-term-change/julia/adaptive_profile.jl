# Julia standard-library example for institutional adaptive profile scoring.

institutions = Dict(
    "City Resilience Office" => [0.70, 0.66, 0.64, 0.72, 0.74, 0.58, 0.72, 0.42, 0.68],
    "Legacy Public Utility" => [0.48, 0.36, 0.54, 0.50, 0.44, 0.42, 0.46, 0.76, 0.46],
    "Participatory Governance Assembly" => [0.72, 0.68, 0.66, 0.86, 0.76, 0.54, 0.70, 0.40, 0.82]
)

function adaptive_profile(v)
    # v = learning, flexibility, coordination, legitimacy, feedback, resources, shock, rigidity, intergenerational
    0.18*v[1] + 0.16*v[2] + 0.16*v[3] + 0.14*v[4] +
    0.14*v[5] + 0.10*v[6] + 0.08*v[7] - 0.10*v[8] + 0.04*v[9]
end

println("institution,adaptive_profile")
for (name, values) in sort(collect(institutions))
    println("$(name),$(round(adaptive_profile(values), digits=4))")
end
