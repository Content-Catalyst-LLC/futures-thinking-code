# Futures Thinking: Scenario Readiness in Julia
# Educational example only.

strategies = Dict(
    "Short-Term Optimization" => [0.88, 0.38, 0.32, 0.34],
    "Incremental Adaptation" => [0.78, 0.60, 0.56, 0.55],
    "Futures-Oriented Strategy" => [0.72, 0.78, 0.74, 0.73],
    "Transformational Strategy" => [0.62, 0.82, 0.84, 0.70]
)

function robustness_score(values)
    mean_performance = sum(values) / length(values)
    worst_case = minimum(values)
    performance_range = maximum(values) - minimum(values)

    return 0.50 * worst_case + 0.30 * mean_performance - 0.20 * performance_range
end

for (strategy, values) in strategies
    println(strategy, ": ", robustness_score(values))
end
