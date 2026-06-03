# Julia standard-library example for Delphi judgment scoring.

judgments = Dict(
    "expert_A_round_1" => [0.66, 0.90, 0.84, 0.58],
    "expert_A_round_2" => [0.68, 0.91, 0.86, 0.60],
    "expert_A_round_3" => [0.69, 0.92, 0.87, 0.61]
)

function judgment_profile(v)
    0.25*v[1] + 0.35*v[2] + 0.25*v[3] + 0.15*v[4]
end

println("judgment,profile")
for (name, values) in sort(collect(judgments))
    println("$(name),$(round(judgment_profile(values), digits=4))")
end
