from src.schema import SchedulingProblem


def explain(problem: SchedulingProblem) -> str:
    explanation = []

    total_workers_available = None
    total_workers_required = None

    skill_available = {}
    skill_required = {}

    for constraint in problem.constraints:

        # --- Capacity ---
        if constraint.type == "capacity":
            rc = constraint.params["resource_count"]
            total_workers_available = rc

            explanation.append(
                f"Total available workers: {rc}."
            )

        # --- Shift Coverage ---
        elif constraint.type == "shift_coverage":
            shifts = constraint.params["shifts"]

            total_workers_required = sum(shifts.values())

            explanation.append(
                f"Shift coverage requires {total_workers_required} total workers "
                f"across shifts {list(shifts.keys())}."
            )

        # --- Skill Coverage ---
        elif constraint.type == "skill_coverage":
            shifts = constraint.params["shifts"]
            available = constraint.params.get("available", {})

            # Count required per skill
            for shift in shifts.values():
                for skill, count in shift.items():
                    skill_required[skill] = skill_required.get(skill, 0) + count

            skill_available = available

            explanation.append(
                f"Skill-based staffing requires: {skill_required}."
            )
            explanation.append(
                f"Available skill capacity: {skill_available}."
            )

        # --- Time Overlap ---
        elif constraint.type == "time_overlap":
            explanation.append(
                "Time overlap constraints were checked."
            )

        # --- Rest Constraint ---
        elif constraint.type == "rest_constraint":
            explanation.append(
                "Rest constraints were checked."
            )

        else:
            explanation.append(
                f"Constraint type '{constraint.type}' is not explainable."
            )

    # --- Capacity Check for Basic Model ---
    if total_workers_available is not None and total_workers_required is not None:
        if total_workers_available >= total_workers_required:
            explanation.append(
                "Overall worker capacity is sufficient."
            )
        else:
            explanation.append(
                "Overall worker capacity is insufficient."
            )

    # --- Skill Capacity Check ---
    if skill_available and skill_required:
        for skill in skill_required:
            required = skill_required.get(skill, 0)
            available = skill_available.get(skill, 0)

            if available < required:
                explanation.append(
                    f"Insufficient {skill} workers: required {required}, available {available}."
                )
            else:
                explanation.append(
                    f"Sufficient {skill} workers."
                )

    return "\n".join(explanation)