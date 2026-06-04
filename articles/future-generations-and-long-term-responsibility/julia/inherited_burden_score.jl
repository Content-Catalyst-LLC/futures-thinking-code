# Julia standard-library example for inherited burden scoring.

profiles = Dict(
    "Stewardship State" => [0.34, 0.32, 0.28, 0.30, 0.82, 0.36, 0.84, 0.80],
    "Short-Term Extraction" => [0.88, 0.76, 0.70, 0.84, 0.38, 0.62, 0.36, 0.24],
    "Reparative Intergenerational Compact" => [0.30, 0.36, 0.32, 0.26, 0.84, 0.34, 0.86, 0.86]
)

function inherited_burden(v)
    # v = climate debt infrastructure ecology institution tech_lock adaptive representation
    0.18*v[1] + 0.14*v[2] + 0.16*v[3] + 0.18*v[4] + 0.14*v[6] +
    0.10*(1-v[5]) + 0.06*(1-v[7]) + 0.04*(1-v[8])
end

println("scenario,inherited_burden")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(inherited_burden(values), digits=4))")
end
