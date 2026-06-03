# Julia standard-library example for anticipatory governance capacity scoring.

profiles = Dict(
    "Reactive Crisis Governance" => [0.36, 0.34, 0.28, 0.42, 0.40, 0.38, 0.32, 0.34, 0.36, 0.48],
    "Participatory Anticipatory Governance" => [0.68, 0.74, 0.78, 0.70, 0.86, 0.72, 0.68, 0.88, 0.78, 0.64],
    "Anticipatory Governance Operating Model" => [0.82, 0.84, 0.82, 0.82, 0.76, 0.78, 0.86, 0.80, 0.84, 0.86]
)

function anticipatory_capacity(v)
    # v = detection interpretation scenario preparedness legitimacy coordination adaptive equity learning implementation
    0.12*v[1] + 0.12*v[2] + 0.12*v[3] + 0.12*v[4] + 0.12*v[5] +
    0.10*v[6] + 0.10*v[7] + 0.08*v[8] + 0.07*v[9] + 0.05*v[10]
end

println("profile,anticipatory_capacity")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(anticipatory_capacity(values), digits=4))")
end
