# Julia standard-library example for early warning score.

signals = Dict(
    "Rising heat-health emergency demand" => [0.58, 0.90, 0.88, 0.82, 0.68, 0.92, 0.80],
    "Public AI appeal failures" => [0.72, 0.86, 0.78, 0.74, 0.74, 0.86, 0.72],
    "Infrastructure service interruptions" => [0.54, 0.88, 0.86, 0.80, 0.62, 0.82, 0.76]
)

function warning_score(v)
    0.12*v[1] + 0.22*v[2] + 0.20*v[3] + 0.13*v[4] + 0.11*v[5] + 0.13*v[6] + 0.09*v[7]
end

println("signal,warning_score")
for (name, values) in sort(collect(signals))
    println("$(name),$(round(warning_score(values), digits=4))")
end
