# Julia standard-library example for weak signal profile scoring.

signals = Dict(
    "Climate insurance withdrawal signal" => [0.48, 0.57, 0.90, 0.82, 0.55, 0.86, 0.88],
    "Community heat-adaptation practice" => [0.29, 0.70, 0.78, 0.74, 0.36, 0.90, 0.82],
    "Unusual AI use pattern" => [0.38, 0.72, 0.77, 0.79, 0.41, 0.78, 0.74]
)

function profile(v)
    0.10*v[1] - 0.08*v[2] + 0.24*v[3] + 0.22*v[4] + 0.12*v[5] + 0.12*v[6] + 0.20*v[7]
end

println("signal,profile")
for (name, values) in sort(collect(signals))
    println("$(name),$(round(profile(values), digits=4))")
end
