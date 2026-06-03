# Futures Literacy and Anticipatory Capacity
# Julia standard-library capacity scoring example.

profiles = Dict(
    "Forecast-Dependent Organization" => [0.32, 0.38, 0.28, 0.24, 0.18, 0.30, 0.42],
    "Scenario-Aware Organization" => [0.64, 0.68, 0.61, 0.70, 0.46, 0.58, 0.66],
    "Futures-Literate Organization" => [0.82, 0.84, 0.88, 0.90, 0.72, 0.84, 0.80],
    "Participatory Anticipatory Institution" => [0.86, 0.82, 0.84, 0.88, 0.94, 0.88, 0.82]
)

weights = [0.15, 0.15, 0.17, 0.13, 0.17, 0.13, 0.10]

function score(values, weights)
    sum(values .* weights)
end

println("organization_type,anticipatory_capacity_score")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(score(values, weights), digits=4))")
end
