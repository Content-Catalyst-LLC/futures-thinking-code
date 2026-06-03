# Julia standard-library example for horizon scanning signal scoring.

signals = Dict(
    "AI public-service accountability concern" => [0.36, 0.66, 0.84, 0.76, 0.68, 0.88, 0.86],
    "Climate insurance withdrawal signal" => [0.48, 0.57, 0.90, 0.82, 0.72, 0.84, 0.91],
    "Community heat-adaptation experiment" => [0.29, 0.70, 0.78, 0.70, 0.82, 0.76, 0.74]
)

function profile(v)
    0.10*v[1] - 0.08*v[2] + 0.22*v[3] + 0.18*v[4] + 0.14*v[5] + 0.14*v[6] + 0.30*v[7]
end

println("signal,profile")
for (name, values) in sort(collect(signals))
    println("$(name),$(round(profile(values), digits=4))")
end
