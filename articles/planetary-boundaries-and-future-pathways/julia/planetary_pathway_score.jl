# Julia standard-library example for planetary pathway scoring.

pathways = Dict(
    "Safe and Just Transformation" => [0.32, 0.30, 0.34, 0.30, 0.32, 0.34, 0.30, 0.36, 0.82, 0.80, 0.84, 0.56, 0.78],
    "Green Growth Acceleration" => [0.42, 0.46, 0.50, 0.44, 0.48, 0.44, 0.38, 0.52, 0.68, 0.64, 0.58, 0.72, 0.54],
    "Extractive Crisis Pathway" => [0.86, 0.88, 0.82, 0.84, 0.78, 0.72, 0.70, 0.82, 0.30, 0.28, 0.24, 0.54, 0.18]
)

function boundary_pressure(v)
    0.16*v[1] + 0.16*v[2] + 0.12*v[3] + 0.12*v[4] + 0.10*v[5] +
    0.10*v[6] + 0.08*v[7] + 0.10*v[8] + 0.06*v[12]
end

function safe_just_score(v)
    p = boundary_pressure(v)
    0.22*v[9] + 0.20*v[10] + 0.20*v[11] + 0.14*v[13] - 0.20*p + 0.04*(1-v[12])
end

println("pathway,boundary_pressure,safe_and_just_score")
for (name, values) in sort(collect(pathways))
    println("$(name),$(round(boundary_pressure(values), digits=4)),$(round(safe_just_score(values), digits=4))")
end
