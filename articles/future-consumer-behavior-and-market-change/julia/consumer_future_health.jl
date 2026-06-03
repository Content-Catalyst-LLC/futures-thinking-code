# Julia standard-library example for consumer future health scoring.

profiles = Dict(
    "Value-Constrained Consumer Economy" => [0.42, 0.48, 0.62, 0.46, 0.44, 0.90, 0.70, 0.52, 0.46, 0.50],
    "Sustainability Becomes Infrastructure" => [0.66, 0.72, 0.68, 0.88, 0.64, 0.58, 0.54, 0.70, 0.64, 0.70],
    "Access and Inclusion Market" => [0.70, 0.76, 0.66, 0.70, 0.86, 0.70, 0.42, 0.68, 0.70, 0.76]
)

function consumer_future_health(v)
    # v = affordability trust digital sustainability access price friction regulation privacy local
    0.14*v[1] + 0.16*v[2] + 0.10*v[4] + 0.16*v[5] + 0.10*(1-v[6]) +
    0.12*(1-v[7]) + 0.06*v[3] + 0.06*v[8] + 0.06*v[9] + 0.04*v[10]
end

println("profile,consumer_future_health")
for (name, values) in sort(collect(profiles))
    println("$(name),$(round(consumer_future_health(values), digits=4))")
end
