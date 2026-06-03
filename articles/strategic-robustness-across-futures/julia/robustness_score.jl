# Julia standard-library example for strategic robustness scoring.

strategies = Dict(
    "Efficiency Optimization" => [0.42, 0.54, 0.66, 0.38],
    "Robust Resilience Portfolio" => [0.66, 0.72, 0.78, 0.70],
    "Adaptive Governance" => [0.64, 0.76, 0.74, 0.82]
)

function worst_case_viability(v)
    minimum(v)
end

println("strategy,worst_case_viability")
for (name, values) in sort(collect(strategies))
    println("$(name),$(round(worst_case_viability(values), digits=4))")
end
