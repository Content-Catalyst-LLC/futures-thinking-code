# Julia standard-library example for future-of-work job quality scoring.

occupations = Dict(
    "Administrative Support" => [0.46, 0.38, 0.42, 0.46, 0.68, 0.62],
    "Care Work" => [0.40, 0.36, 0.44, 0.40, 0.54, 0.55],
    "Knowledge Work" => [0.66, 0.54, 0.72, 0.60, 0.46, 0.70]
)

function job_quality(v)
    # v = wage_security, worker_voice, training, protection, surveillance, initial_quality
    0.28*v[6] + 0.18*v[1] + 0.18*v[2] + 0.16*v[4] + 0.12*v[3] + 0.08*(1 - v[5])
end

println("occupation,adjusted_job_quality_score")
for (name, values) in sort(collect(occupations))
    println("$(name),$(round(job_quality(values), digits=4))")
end
