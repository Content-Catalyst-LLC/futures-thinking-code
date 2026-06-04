# Julia standard-library example for global governance capacity scoring.

profiles = Dict(
    "Multilateral Renewal" => [0.78, 0.76, 0.74, 0.70, 0.76, 0.68, 0.74, 0.78, 0.72, 0.70],
    "Democratic and Justice-Centered Governance" => [0.82, 0.88, 0.78, 0.80, 0.84, 0.78, 0.86, 0.88, 0.90, 0.92],
    "Governance Breakdown" => [0.22, 0.18, 0.20, 0.24, 0.18, 0.22, 0.20, 0.18, 0.16, 0.14]
)

function governance_capacity(v)
    # v = institutional legitimacy law finance collective tech planetary adaptive accountability representation
    0.14*v[1] + 0.16*v[2] + 0.12*v[3] + 0.11*v[4] + 0.13*v[5] +
    0.10*v[6] + 0.10*v[7] + 0.08*v[8] + 0.08*v[9] + 0.08*v[10]
end

println("profile,governance_capacity")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(governance_capacity(values), digits=4))")
end
