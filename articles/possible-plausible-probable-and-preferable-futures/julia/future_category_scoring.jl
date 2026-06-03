# Julia standard-library scoring example.

futures = Dict(
    "AI-Augmented Public Services" => [0.82, 0.76, 0.68, 0.80, 0.58, 0.52, 0.60, 0.54],
    "Participatory Anticipatory Governance" => [0.62, 0.70, 0.56, 0.42, 0.86, 0.78, 0.84, 0.90],
    "Regenerative Urban Systems" => [0.58, 0.64, 0.52, 0.36, 0.90, 0.94, 0.88, 0.82]
)

function scores(v)
    plausibility = 0.40*v[1] + 0.35*v[2] + 0.25*v[3]
    probability = 0.70*v[4] + 0.30*v[1]
    preference = 0.30*v[5] + 0.25*v[6] + 0.25*v[7] + 0.20*v[8]
    priority = 0.35*plausibility + 0.25*probability + 0.40*preference
    return plausibility, probability, preference, priority
end

println("future,plausibility,probability,preference,priority")
for (name, values) in sort(collect(futures))
    p1, p2, p3, p4 = scores(values)
    println("$(name),$(round(p1,digits=4)),$(round(p2,digits=4)),$(round(p3,digits=4)),$(round(p4,digits=4))")
end
