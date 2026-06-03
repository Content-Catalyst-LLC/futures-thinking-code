# Julia standard-library example for driver priority scoring.

drivers = Dict(
    "Public trust and institutional legitimacy" => [0.88, 0.82, 0.80, 0.84, 0.84, 0.70, 0.68, 0.54],
    "Public-sector AI accountability capacity" => [0.84, 0.78, 0.78, 0.76, 0.88, 0.74, 0.72, 0.62],
    "Regional food-water-ecology stress" => [0.88, 0.74, 0.80, 0.88, 0.88, 0.68, 0.74, 0.38]
)

function driver_priority(v)
    0.22*v[1] + 0.20*v[2] + 0.14*v[3] + 0.14*v[4] + 0.12*v[5] + 0.08*v[6] + 0.06*v[7] + 0.04*(1-v[8])
end

println("driver,priority")
for (name, values) in sort(collect(drivers))
    println("$(name),$(round(driver_priority(values), digits=4))")
end
