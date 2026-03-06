from ortools.sat.python import cp_model


def apply_shift_coverage(context, constraint):
    model = context["model"]
    assign = context["assign"]
    nurses = context["nurses"]
    shift_names = context["shift_names"]

    shifts = constraint.params["shifts"]

    for shift in shift_names:
        model.Add(
            sum(assign[(nurse["id"], shift)] for nurse in nurses)
            == shifts[shift]
        )

def apply_skill_coverage(context, constraint):
    model = context["model"]
    assign = context["assign"]
    nurses = context["nurses"]

    skill_coverage = constraint.params["shifts"]

    for shift, skill_requirements in skill_coverage.items():
        for skill, required in skill_requirements.items():
            model.Add(
                sum(
                    assign[(nurse["id"], shift)]
                    for nurse in nurses
                    if nurse["skill"] == skill
                ) == required
            )

def apply_rest_constraint(context, constraint):
    model = context["model"]
    assign = context["assign"]
    nurses = context["nurses"]
    shift_names = context["shift_names"]

    max_consecutive = constraint.params["max_consecutive"]

    for nurse in nurses:
        for i in range(len(shift_names) - max_consecutive):
            model.Add(
                sum(
                    assign[(nurse["id"], shift_names[j])]
                    for j in range(i, i + max_consecutive + 1)
                )
                <= max_consecutive
            )

def apply_capacity(context, constraint):
    resource_count = (
        constraint.params.get("resource_count") or
        constraint.params.get("total_workers") or
        0
    )
    if resource_count == 0:
        print("⚠️ Warning: capacity constraint has 0 workers")
    
    if "capacity_total" not in context:
        context["capacity_total"] = 0
        
    context["capacity_total"] += resource_count

def apply_time_overlap(context, constraint):
    model = context["model"]
    assign = context["assign"]
    nurses = context["nurses"]

    shifts = constraint.params["shifts"]

    # build overlap pairs
    for i in range(len(shifts)):
        for j in range(i + 1, len(shifts)):
            s1 = shifts[i]
            s2 = shifts[j]

            if not (s1["end"] <= s2["start"] or s2["end"] <= s1["start"]):
                for nurse in nurses:
                    model.Add(
                        assign[(nurse["id"], s1["name"])]
                        + assign[(nurse["id"], s2["name"])]
                        <= 1
                    )

HANDLER_REGISTRY = {
    "capacity": apply_capacity,
    "shift_coverage": apply_shift_coverage,
    "skill_coverage": apply_skill_coverage,
    "rest_constraint": apply_rest_constraint,
    "time_overlap": apply_time_overlap,
}