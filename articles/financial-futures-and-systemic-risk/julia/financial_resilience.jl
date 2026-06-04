# Julia standard-library example for financial resilience scoring.

profiles = Dict(
    "Resilient Public-Interest Finance" => [0.42, 0.82, 0.80, 0.44, 0.48, 0.38, 0.86, 0.78, 0.84, 0.76],
    "Debt-Fragile Household Economy" => [0.74, 0.44, 0.30, 0.52, 0.54, 0.50, 0.46, 0.42, 0.38, 0.44],
    "Shadow Finance Stress" => [0.82, 0.42, 0.48, 0.50, 0.90, 0.62, 0.42, 0.48, 0.44, 0.52]
)

function financial_resilience(v)
    # v = leverage liquidity household climate nonbank digital regulation public consumer productive
    0.14*v[2] + 0.14*v[3] + 0.14*v[7] + 0.10*v[8] + 0.10*v[9] +
    0.10*v[10] + 0.10*(1-v[1]) + 0.08*(1-v[4]) + 0.06*(1-v[5]) + 0.04*(1-v[6])
end

println("profile,financial_resilience")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(financial_resilience(values), digits=4))")
end
