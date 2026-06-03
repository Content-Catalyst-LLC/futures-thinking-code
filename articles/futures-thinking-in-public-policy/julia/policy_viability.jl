# Julia standard-library example for public policy futures profile scoring.

policies = Dict(
    "Short-Term Reactive Policy" => [0.38, 0.42, 0.36, 0.44, 0.40, 0.62, 0.34, 0.28],
    "Adaptive Long-Horizon Policy" => [0.82, 0.69, 0.84, 0.73, 0.68, 0.62, 0.78, 0.76],
    "Participatory Anticipatory Policy" => [0.80, 0.84, 0.82, 0.76, 0.86, 0.56, 0.82, 0.84]
)

function policy_futures_profile(v)
    # v = robustness, equity, adaptability, coordination, legitimacy, implementation, learning, intergenerational
    0.20*v[1] + 0.16*v[2] + 0.18*v[3] + 0.14*v[4] +
    0.14*v[5] + 0.08*v[6] + 0.06*v[7] + 0.04*v[8]
end

println("policy,policy_futures_profile")
for (name, values) in sort(collect(policies))
    println("$(name),$(round(policy_futures_profile(values), digits=4))")
end
