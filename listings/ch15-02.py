def select_model(task, envelope, candidates):
    admissible = []

    for candidate in candidates:
        if not candidate.is_certified_for(task.role):
            continue
        if candidate.zone not in envelope.permitted_zones:
            continue
        if candidate.processing_jurisdiction not in envelope.permitted_jurisdictions:
            continue
        if not retention_compatible(candidate, envelope):
            continue
        if not network_path_compatible(candidate, envelope):
            continue
        if not key_profile_compatible(candidate, envelope):
            continue
        admissible.append(candidate)

    if not admissible:
        return escalate_or_fail_secure(task, envelope)

    return optimize_within_admissible_set(
        admissible,
        quality=task.required_quality,
        latency=task.latency_budget,
        cost=task.cost_budget
    )
