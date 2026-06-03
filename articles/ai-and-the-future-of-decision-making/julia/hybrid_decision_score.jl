# Julia standard-library example for AI hybrid decision-system scoring.

systems = Dict(
    "Human-Centered System" => [0.82, 0.28, 0.54, 0.76, 0.61, 0.74, 0.70, 0.66],
    "High-Governance Hybrid System" => [0.72, 0.74, 0.83, 0.79, 0.78, 0.82, 0.80, 0.76],
    "Public-Interest Decision Infrastructure" => [0.76, 0.70, 0.86, 0.84, 0.80, 0.88, 0.86, 0.84]
)

function decision_profile(v)
    0.16*v[1] + 0.16*v[2] + 0.16*v[3] + 0.12*v[4] + 0.12*v[5] + 0.12*v[6] + 0.08*v[7] + 0.08*v[8]
end

println("system,decision_system_profile_score")
for (name, values) in sort(collect(systems))
    println("$(name),$(round(decision_profile(values), digits=4))")
end
