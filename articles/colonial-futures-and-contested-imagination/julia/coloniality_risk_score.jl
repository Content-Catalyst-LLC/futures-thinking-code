# Julia standard-library example for coloniality risk scoring.

profiles = Dict(
    "Green Extraction Continuity" => [0.86, 0.34, 0.90, 0.82, 0.36, 0.38, 0.78, 0.24, 0.30, 0.28, 0.44],
    "Reparative Plural Futures" => [0.34, 0.86, 0.38, 0.30, 0.88, 0.82, 0.28, 0.92, 0.90, 0.78, 0.82],
    "Data Colonial Futures" => [0.88, 0.28, 0.48, 0.92, 0.30, 0.34, 0.54, 0.26, 0.30, 0.20, 0.38]
)

function coloniality_risk(v)
    # v = agenda consent land external epistemic benefit harm repair sovereignty data labor
    0.12*v[1] + 0.12*(1-v[2]) + 0.12*v[3] + 0.12*v[4] + 0.11*(1-v[5]) +
    0.10*(1-v[6]) + 0.10*v[7] + 0.09*(1-v[8]) + 0.07*(1-v[9]) +
    0.03*(1-v[10]) + 0.02*(1-v[11])
end

println("future,coloniality_risk")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(coloniality_risk(values), digits=4))")
end
