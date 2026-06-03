# Julia standard-library example for public-sector foresight capacity scoring.

models = Dict(
    "Ad Hoc Foresight Workshop" => [0.32, 0.46, 0.24, 0.28, 0.18, 0.22, 0.26, 0.20, 0.24, 0.34],
    "Budget-Integrated Foresight System" => [0.66, 0.74, 0.82, 0.58, 0.88, 0.72, 0.76, 0.84, 0.70, 0.66],
    "Participatory Public Foresight System" => [0.68, 0.78, 0.68, 0.90, 0.62, 0.76, 0.80, 0.60, 0.72, 0.86]
)

function foresight_capacity(v)
    # v = scanning, scenarios, uptake, participation, budget, evaluation, learning, authority, knowledge, legitimacy
    0.12*v[1] + 0.12*v[2] + 0.14*v[3] + 0.12*v[4] + 0.12*v[5] +
    0.10*v[6] + 0.10*v[7] + 0.10*v[8] + 0.05*v[9] + 0.03*v[10]
end

println("model,foresight_capacity")
for (name, values) in sort(collect(models))
    println("$(name),$(round(foresight_capacity(values), digits=4))")
end
