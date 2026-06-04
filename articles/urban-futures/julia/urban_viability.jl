# Julia standard-library example for urban viability scoring.

profiles = Dict(
    "Adaptive Public City" => [0.78, 0.78, 0.74, 0.42, 0.40, 0.68, 0.76, 0.74, 0.34],
    "Financialized Growth City" => [0.66, 0.48, 0.30, 0.56, 0.82, 0.72, 0.50, 0.34, 0.50],
    "Governance Breakdown City" => [0.46, 0.28, 0.34, 0.68, 0.80, 0.42, 0.30, 0.32, 0.82]
)

function urban_viability(v)
    # v = infrastructure governance housing climate inequality digital finance cohesion maintenance
    0.17*v[1] + 0.16*v[2] + 0.14*v[3] - 0.14*v[4] - 0.14*v[5] +
    0.09*v[6] + 0.12*v[7] + 0.14*v[8] - 0.08*v[9]
end

println("profile,urban_viability")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(urban_viability(values), digits=4))")
end
