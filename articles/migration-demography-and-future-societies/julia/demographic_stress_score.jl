# Julia standard-library example for demographic stress scoring.

profiles = Dict(
    "Aging Without Care Reform" => [0.92, 0.42, 0.44, 0.28, 0.62, 0.42, 0.38, 0.48, 0.50, 0.56],
    "Rights-Based Migration Renewal" => [0.58, 0.46, 0.54, 0.66, 0.60, 0.74, 0.42, 0.72, 0.70, 0.68],
    "Demographic Fear Politics" => [0.62, 0.70, 0.80, 0.34, 0.74, 0.36, 0.62, 0.22, 0.28, 0.38]
)

function demographic_stress(v)
    # v = aging youth migration care housing labor climate cohesion gender health
    0.13*v[1] + 0.13*v[2] + 0.12*v[3] + 0.13*(1-v[4]) + 0.12*v[5] +
    0.10*(1-v[6]) + 0.11*v[7] + 0.08*(1-v[8]) + 0.05*(1-v[9]) + 0.03*(1-v[10])
end

println("profile,demographic_stress")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(demographic_stress(values), digits=4))")
end
