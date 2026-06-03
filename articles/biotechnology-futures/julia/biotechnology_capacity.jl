# Julia standard-library example for responsible biotechnology capacity.

scenarios = Dict(
    "Public-Interest Bioinnovation" => [0.72, 0.78, 0.76, 0.80, 0.68, 0.74, 0.42, 0.36],
    "Bioeconomy Acceleration" => [0.78, 0.48, 0.48, 0.44, 0.84, 0.36, 0.56, 0.58],
    "Democratic Biofutures" => [0.68, 0.82, 0.84, 0.86, 0.62, 0.88, 0.46, 0.34]
)

function responsible_capacity(v)
    0.16*v[1] + 0.18*v[2] + 0.16*v[3] + 0.16*v[4] +
    0.12*v[5] + 0.12*v[6] + 0.05*(1 - v[7]) + 0.05*(1 - v[8])
end

println("scenario,responsible_biotechnology_capacity")
for (name, values) in sort(collect(scenarios))
    println("$(name),$(round(responsible_capacity(values), digits=4))")
end
