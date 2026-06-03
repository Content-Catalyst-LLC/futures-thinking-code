# Julia standard-library example for trend and megatrend profile scoring.

patterns = Dict(
    "Digital Labor Restructuring" => [0.78, 0.71, 0.76, 0.34, 0.58, 0.72],
    "Climate Risk Intensification" => [0.74, 0.86, 0.88, 0.22, 0.52, 0.86],
    "Population Aging" => [0.69, 0.81, 0.79, 0.28, 0.46, 0.70],
    "Urban Heat and Housing Stress" => [0.70, 0.82, 0.84, 0.26, 0.54, 0.90]
)

function profile(v)
    0.20*v[1] + 0.22*v[2] + 0.22*v[3] - 0.12*v[4] - 0.14*v[5] + 0.10*v[6]
end

println("pattern,profile")
for (name, values) in sort(collect(patterns))
    println("$(name),$(round(profile(values), digits=4))")
end
