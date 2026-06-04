# Julia standard-library example for disciplined hope scoring.

profiles = Dict(
    "Disciplined Hope Democracy" => [0.78, 0.82, 0.72, 0.78, 0.84, 0.76, 0.30, 0.34],
    "Apocalyptic Paralysis" => [0.18, 0.22, 0.20, 0.24, 0.28, 0.20, 0.82, 0.60],
    "Reparative Imagination" => [0.86, 0.84, 0.76, 0.80, 0.88, 0.92, 0.28, 0.30]
)

function disciplined_hope(v)
    # v = hope agency trust institution accountability repair fatigue polarization
    0.18*v[1] + 0.18*v[2] + 0.16*v[3] + 0.16*v[4] + 0.14*v[5] +
    0.12*v[6] - 0.04*v[7] - 0.02*v[8]
end

println("scenario,disciplined_hope")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(disciplined_hope(values), digits=4))")
end
