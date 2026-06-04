# Julia standard-library example for foresight capability scoring.

profiles = Dict(
    "Government Agency" => [0.62, 0.66, 0.57, 0.63, 0.51, 0.52, 0.56, 0.58],
    "Climate Adaptation Authority" => [0.76, 0.74, 0.72, 0.70, 0.66, 0.66, 0.72, 0.68],
    "Civil Society Coalition" => [0.64, 0.60, 0.68, 0.44, 0.62, 0.84, 0.82, 0.46]
)

function foresight_capability(v)
    # v = signal scenario learning governance adaptive participation ethics data
    0.16*v[1] + 0.16*v[2] + 0.14*v[3] + 0.14*v[4] +
    0.12*v[5] + 0.10*v[6] + 0.10*v[7] + 0.08*v[8]
end

println("institution,foresight_capability")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(foresight_capability(values), digits=4))")
end
