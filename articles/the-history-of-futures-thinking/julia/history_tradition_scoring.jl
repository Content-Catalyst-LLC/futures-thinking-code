# Julia standard-library scoring example for historical futures traditions.

traditions = Dict(
    "Military and Strategic Planning" => [0.90, 0.94, 0.20, 0.36, 0.76],
    "Systems and Ecological Futures" => [0.88, 0.74, 0.42, 0.68, 0.96],
    "Participatory and Democratic Futures" => [0.68, 0.42, 0.92, 0.86, 0.64],
    "Decolonial and Indigenous Futures" => [0.70, 0.36, 0.88, 0.94, 0.72]
)

function reflective_score(v)
    0.25*v[1] + 0.25*v[3] + 0.25*v[4] + 0.25*v[5]
end

function power_risk(v)
    v[2] * (1 - v[3]) * (1 - v[4])
end

println("tradition,reflective_score,power_risk")
for (name, values) in sort(collect(traditions))
    println("$(name),$(round(reflective_score(values), digits=4)),$(round(power_risk(values), digits=4))")
end
