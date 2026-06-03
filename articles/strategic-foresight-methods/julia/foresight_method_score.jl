# Julia standard-library example for strategic foresight method scoring.

methods = Dict(
    "Horizon Scanning" => [0.86, 0.72, 0.48, 0.46, 0.42, 0.68, 0.74],
    "Scenario Planning" => [0.42, 0.82, 0.84, 0.72, 0.62, 0.76, 0.86],
    "Backcasting" => [0.30, 0.66, 0.78, 0.90, 0.68, 0.66, 0.82],
    "Causal Layered Analysis" => [0.38, 0.88, 0.82, 0.62, 0.72, 0.54, 0.88]
)

weights = [0.16, 0.14, 0.16, 0.18, 0.14, 0.10, 0.12]

function score(values, weights)
    sum(values .* weights)
end

println("method,profile_score")
for (name, values) in sort(collect(methods))
    println("$(name),$(round(score(values, weights), digits=4))")
end
