# Dynamic uncertainty and robustness example for Futures Thinking.
# Uses only Julia standard functionality.

strategies = Dict(
    "Forecast-Optimized Strategy" => [0.91, 0.42, 0.38, 0.36, 0.49],
    "Flexible Foresight Strategy" => [0.78, 0.76, 0.74, 0.71, 0.79],
    "Transformational Strategy" => [0.62, 0.82, 0.85, 0.77, 0.88],
    "Defensive Continuity Strategy" => [0.70, 0.52, 0.56, 0.61, 0.57],
    "Participatory Futures Strategy" => [0.66, 0.72, 0.78, 0.80, 0.86]
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
