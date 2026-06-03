# Julia standard-library example for structural pressure scoring.

systems = Dict(
    "Climate Adaptation" => [0.86, 0.46, 0.52, 0.88, 0.90],
    "Institutional Trust" => [0.76, 0.38, 0.36, 0.78, 0.82],
    "Food-Water-Ecology" => [0.84, 0.48, 0.54, 0.90, 0.84]
)

function structural_pressure(v)
    0.26*v[1] + 0.22*(1-v[2]) + 0.18*(1-v[3]) + 0.18*v[4] + 0.16*v[5]
end

println("system,structural_pressure")
for (name, values) in sort(collect(systems))
    println("$(name),$(round(structural_pressure(values), digits=4))")
end
