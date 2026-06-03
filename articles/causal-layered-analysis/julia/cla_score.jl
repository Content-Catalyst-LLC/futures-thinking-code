# Julia standard-library example for CLA depth scoring.

issues = Dict(
    "Public AI accountability" => [0.84, 0.78, 0.88, 0.82, 0.90, 0.92, 0.88],
    "Climate adaptation and housing" => [0.90, 0.88, 0.84, 0.86, 0.88, 0.94, 0.92],
    "Education for uncertain futures" => [0.72, 0.74, 0.90, 0.92, 0.92, 0.78, 0.82]
)

function cla_depth(v)
    0.10*v[1] + 0.18*v[2] + 0.22*v[3] + 0.20*v[4] + 0.16*v[5] + 0.08*v[6] + 0.06*v[7]
end

println("issue,cla_depth")
for (name, values) in sort(collect(issues))
    println("$(name),$(round(cla_depth(values), digits=4))")
end
