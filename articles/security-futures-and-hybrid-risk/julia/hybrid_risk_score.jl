# Julia standard-library example for hybrid security risk scoring.

profiles = Dict(
    "Managed Hybrid Competition" => [0.54, 0.62, 0.52, 0.44, 0.50, 0.70, 0.66, 0.72, 0.68, 0.62],
    "Human Security and Resilience Renewal" => [0.42, 0.56, 0.38, 0.42, 0.46, 0.82, 0.88, 0.86, 0.84, 0.74],
    "Systemic Security Breakdown" => [0.88, 0.92, 0.90, 0.88, 0.84, 0.22, 0.20, 0.18, 0.16, 0.22]
)

function hybrid_risk(v)
    # v = cyber infra info climate resource coordination protection adaptive trust attribution
    0.13*v[1] + 0.13*v[2] + 0.13*v[3] + 0.12*v[4] + 0.10*v[5] +
    0.11*(1-v[6]) + 0.10*(1-v[7]) + 0.10*(1-v[8]) + 0.05*(1-v[9]) + 0.03*(1-v[10])
end

println("profile,hybrid_risk")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(hybrid_risk(values), digits=4))")
end
