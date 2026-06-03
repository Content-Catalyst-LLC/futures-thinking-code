# Julia standard-library example for scenario viability scoring.

strategies = Dict(
    "Efficiency Optimization" => [1.42, 0.82, 1.14, 0.09],
    "Robust Resilience Portfolio" => [1.55, 1.02, 1.28, 0.15],
    "Adaptive Governance" => [1.61, 0.98, 1.30, 0.18]
)

function viability(v)
    0.35*v[1] + 0.30*v[2] + 0.20*v[3] + 0.15*v[4]
end

println("strategy,viability")
for (name, values) in sort(collect(strategies))
    println("$(name),$(round(viability(values), digits=4))")
end
