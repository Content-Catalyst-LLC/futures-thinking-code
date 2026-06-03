# Julia standard-library example for backcasting pathway scoring.

pathways = Dict(
    "Integrated Climate Infrastructure Pathway" => [0.68, 0.60, 0.58, 0.70, 0.84, 0.76, 0.78, 0.42],
    "Public Accountability Before Scale" => [0.66, 0.56, 0.52, 0.78, 0.72, 0.86, 0.80, 0.40],
    "Participatory Just Energy Transition" => [0.64, 0.62, 0.52, 0.86, 0.82, 0.90, 0.80, 0.44]
)

function viability(v)
    0.18*v[1] - 0.16*v[2] + 0.14*v[3] + 0.18*v[4] + 0.16*v[5] + 0.12*v[6] + 0.14*v[7] - 0.12*v[8]
end

println("pathway,viability")
for (name, values) in sort(collect(pathways))
    println("$(name),$(round(viability(values), digits=4))")
end
