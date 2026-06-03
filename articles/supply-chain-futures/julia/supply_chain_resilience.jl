# Julia standard-library example for supply chain resilience scoring.

profiles = Dict(
    "Lowest-Cost Global Efficiency" => [0.90, 0.34, 0.24, 0.42, 0.36, 0.30, 0.44, 0.26, 0.38, 0.38],
    "Regional Resilience Shift" => [0.58, 0.78, 0.70, 0.66, 0.64, 0.62, 0.64, 0.48, 0.66, 0.74],
    "Essential Goods Resilience Model" => [0.52, 0.76, 0.84, 0.74, 0.72, 0.70, 0.76, 0.54, 0.80, 0.86]
)

function resilience_score(v)
    # v = cost diversification buffer visibility labor climate traceability circularity regulation recovery
    0.10*v[1] + 0.16*v[2] + 0.14*v[3] + 0.14*v[4] + 0.12*v[5] +
    0.13*v[6] + 0.09*v[7] + 0.06*v[8] + 0.04*v[9] + 0.02*v[10]
end

println("profile,supply_chain_resilience")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(resilience_score(values), digits=4))")
end
