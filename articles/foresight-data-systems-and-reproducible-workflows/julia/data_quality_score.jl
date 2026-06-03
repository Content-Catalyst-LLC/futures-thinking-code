records = Dict("Climate exposure and compound hazards" => [1.00, 1.00, 0.82, 0.86], "Public trust and institutional legitimacy" => [1.00, 0.95, 0.78, 0.70], "AI accountability capacity" => [0.90, 0.95, 0.80, 0.74])
function data_quality(v)
    0.25*v[1] + 0.25*v[2] + 0.25*v[3] + 0.25*v[4]
end
println("record,data_quality_score")
for (name, values) in sort(collect(records))
    println("$(name),$(round(data_quality(values), digits=4))")
end
