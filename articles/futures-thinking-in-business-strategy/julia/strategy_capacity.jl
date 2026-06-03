# Julia standard-library example for business futures readiness scoring.

strategies = Dict(
    "Efficiency-Driven Legacy Strategy" => [0.38, 0.74, 0.41, 0.33, 0.62, 0.36, 0.44, 0.48, 0.34],
    "Adaptive Innovation Strategy" => [0.82, 0.52, 0.72, 0.79, 0.68, 0.80, 0.66, 0.70, 0.76],
    "Resilient Portfolio Strategy" => [0.64, 0.49, 0.81, 0.76, 0.73, 0.68, 0.70, 0.72, 0.70]
)

function futures_readiness(v)
    # v = innovation, exposure, resilience, flexibility, alignment, sensing, capital, legitimacy, transition
    0.14*v[1] - 0.10*v[2] + 0.15*v[3] + 0.14*v[4] + 0.10*v[5] +
    0.12*v[6] + 0.08*v[7] + 0.09*v[8] + 0.08*v[9]
end

println("strategy,business_futures_readiness")
for (name, values) in sort(collect(strategies))
    println("$(name),$(round(futures_readiness(values), digits=4))")
end
