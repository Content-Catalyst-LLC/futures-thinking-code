strategies = Dict(
    "Forecast-Optimized Strategy" => [0.91, 0.42, 0.38, 0.36, 0.40, 0.34],
    "Flexible Foresight Strategy" => [0.78, 0.75, 0.72, 0.70, 0.73, 0.69],
    "Transformational Strategy" => [0.62, 0.81, 0.84, 0.76, 0.78, 0.74],
    "Defensive Continuity Strategy" => [0.70, 0.52, 0.55, 0.58, 0.57, 0.60]
)

function mean_value(values)
    return sum(values) / length(values)
end

function std_value(values)
    mu = mean_value(values)
    return sqrt(sum((x - mu)^2 for x in values) / length(values))
end

println("Strategy,Mean,Worst,Best,Robustness")
for (strategy, values) in strategies
    mu = mean_value(values)
    worst = minimum(values)
    best = maximum(values)
    vol = std_value(values)
    robustness = 0.45 * worst + 0.35 * mu - 0.20 * vol
    println("$(strategy),$(round(mu, digits=4)),$(worst),$(best),$(round(robustness, digits=4))")
end
