# Julia standard-library example for energy transition readiness.

scenarios = Dict(
    "Managed Just Transition" => [0.82, 0.78, 0.74, 0.76, 0.78, 0.84, 0.82, 0.76, 0.80],
    "Renewables Without Grids" => [0.84, 0.34, 0.38, 0.54, 0.56, 0.44, 0.42, 0.48, 0.46],
    "Resilient Distributed Energy Future" => [0.76, 0.72, 0.80, 0.72, 0.68, 0.82, 0.74, 0.72, 0.86]
)

function transition_readiness(v)
    # v = clean, grid, storage, electrification, phase_down, justice, labor, materials, resilience
    0.14*v[1] + 0.14*v[2] + 0.12*v[3] + 0.12*v[4] + 0.12*v[5] +
    0.12*v[6] + 0.10*v[7] + 0.08*v[8] + 0.06*v[9]
end

println("scenario,transition_readiness")
for (name, values) in sort(collect(scenarios))
    println("$(name),$(round(transition_readiness(values), digits=4))")
end
