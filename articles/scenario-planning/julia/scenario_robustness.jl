# Julia standard-library example for scenario strategy robustness.

strategies = Dict(
    "Efficiency-Optimized Strategy" => [0.84, 0.42, 0.35, 0.38, 0.46],
    "Robust Adaptive Strategy" => [0.74, 0.76, 0.73, 0.70, 0.80],
    "Innovation-Bet Strategy" => [0.62, 0.84, 0.44, 0.48, 0.58],
    "Resilience-First Strategy" => [0.66, 0.68, 0.82, 0.74, 0.76],
    "Participatory Futures Strategy" => [0.61, 0.70, 0.76, 0.82, 0.88]
)

function mean_value(values)
    sum(values) / length(values)
end

function std_value(values)
    μ = mean_value(values)
    sqrt(sum((x - μ)^2 for x in values) / length(values))
end

function robustness(values)
    μ = mean_value(values)
    worst = minimum(values)
    volatility = std_value(values)
    0.55 * worst + 0.35 * μ - 0.10 * volatility
end

println("strategy,mean,worst,best,volatility,robustness")
for (strategy, values) in sort(collect(strategies))
    println(
        strategy, ",",
        round(mean_value(values), digits=4), ",",
        round(minimum(values), digits=4), ",",
        round(maximum(values), digits=4), ",",
        round(std_value(values), digits=4), ",",
        round(robustness(values), digits=4)
    )
end
