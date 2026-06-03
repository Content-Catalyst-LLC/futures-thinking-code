# Julia standard-library example for future-ready regulatory capacity scoring.

models = Dict(
    "Reactive Compliance Regulation" => [0.30, 0.42, 0.58, 0.46, 0.28, 0.34, 0.36, 0.40, 0.70, 0.42],
    "Adaptive Regulation" => [0.78, 0.80, 0.70, 0.68, 0.58, 0.86, 0.82, 0.62, 0.60, 0.64],
    "Rights-Centered Technology Regulation" => [0.70, 0.76, 0.78, 0.90, 0.62, 0.72, 0.74, 0.72, 0.66, 0.86]
)

function regulatory_capacity(v)
    # v = foresight, monitoring, enforcement, rights, participation, revision, learning, capture, certainty, remedy
    0.13*v[1] + 0.12*v[2] + 0.12*v[3] + 0.14*v[4] + 0.10*v[5] +
    0.12*v[6] + 0.10*v[7] + 0.08*v[8] + 0.05*v[9] + 0.04*v[10]
end

println("model,future_ready_regulatory_capacity")
for (name, values) in sort(collect(models))
    println("$(name),$(round(regulatory_capacity(values), digits=4))")
end
