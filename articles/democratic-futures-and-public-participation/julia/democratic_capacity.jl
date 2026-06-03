# Julia standard-library example for democratic futures capacity scoring.

models = Dict(
    "Late-Stage Public Consultation" => [0.42, 0.34, 0.38, 0.26, 0.30, 0.32, 0.36, 0.22, 0.40, 0.20],
    "Citizen Assembly" => [0.78, 0.88, 0.84, 0.64, 0.70, 0.68, 0.82, 0.66, 0.76, 0.58],
    "Co-Governance Futures Board" => [0.82, 0.78, 0.80, 0.78, 0.82, 0.84, 0.78, 0.80, 0.76, 0.86]
)

function democratic_capacity(v)
    # v = inclusion, deliberation, representation, uptake, accountability, justice, learning, influence, accessibility, community_authority
    0.11*v[1] + 0.12*v[2] + 0.11*v[3] + 0.14*v[4] + 0.12*v[5] +
    0.12*v[6] + 0.08*v[7] + 0.10*v[8] + 0.05*v[9] + 0.05*v[10]
end

println("model,democratic_futures_capacity")
for (name, values) in sort(collect(models))
    println("$(name),$(round(democratic_capacity(values), digits=4))")
end
