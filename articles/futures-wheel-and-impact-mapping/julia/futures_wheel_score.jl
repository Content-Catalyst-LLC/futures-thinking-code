# Julia standard-library example for Futures Wheel consequence scoring.

consequences = Dict(
    "Energy affordability stress" => [0.78, 0.84, 0.44, 0.92, 0.74],
    "Heat-related health emergencies" => [0.84, 0.90, 0.36, 0.94, 0.78],
    "Appeal and due-process failures increase" => [0.74, 0.88, 0.50, 0.92, 0.74]
)

function consequence_priority(v)
    0.22*v[1] + 0.26*v[2] + 0.14*v[3] + 0.22*v[4] + 0.16*v[5]
end

println("consequence,priority")
for (name, values) in sort(collect(consequences))
    println("$(name),$(round(consequence_priority(values), digits=4))")
end
