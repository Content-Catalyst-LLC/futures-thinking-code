# Julia standard-library example for public-interest platform capacity.

scenarios = Dict(
    "Platform Enclosure" => [0.88, 0.86, 0.22, 0.24, 0.26, 0.30, 0.28, 0.24],
    "Interoperable Platform Ecosystems" => [0.48, 0.52, 0.84, 0.58, 0.72, 0.78, 0.58, 0.78],
    "Digital Public Infrastructure Turn" => [0.42, 0.46, 0.76, 0.70, 0.82, 0.84, 0.70, 0.86]
)

function public_interest_capacity(v)
    # v = platform_power, data_advantage, interoperability, worker_protection,
    # public_accountability, user_rights, ecological_responsibility, digital_public_value
    0.18*v[3] + 0.18*v[5] + 0.16*v[6] + 0.14*v[4] +
    0.14*v[8] + 0.10*v[7] + 0.05*(1 - v[1]) + 0.05*(1 - v[2])
end

println("scenario,public_interest_platform_capacity")
for (name, values) in sort(collect(scenarios))
    println("$(name),$(round(public_interest_capacity(values), digits=4))")
end
