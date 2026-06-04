# Julia standard-library example for ethical futures profile scoring.

profiles = Dict(
    "Technology Firm" => [0.46, 0.41, 0.38, 0.35, 0.33, 0.30, 0.42, 0.52, 0.36, 0.34],
    "Civil Society Coalition" => [0.72, 0.84, 0.76, 0.82, 0.78, 0.80, 0.74, 0.72, 0.86, 0.82],
    "Security Agency" => [0.56, 0.38, 0.46, 0.40, 0.42, 0.34, 0.70, 0.56, 0.36, 0.38]
)

function ethical_profile(v)
    # v = intergenerational inclusion accountability risk_equity transparency contestability precaution learning epistemic legitimacy
    0.13*v[1] + 0.12*v[2] + 0.12*v[3] + 0.12*v[4] + 0.10*v[5] +
    0.10*v[6] + 0.10*v[7] + 0.08*v[8] + 0.08*v[9] + 0.05*v[10]
end

println("institution,ethical_futures_profile")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(ethical_profile(values), digits=4))")
end
