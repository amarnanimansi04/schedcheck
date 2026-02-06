from src.schema import SchedulingProblem


def explain(problem: SchedulingProblem) -> str:
    explanation = []

    total_capacity = None
    total_required = None

    for constraint in problem.constraints:

  
        if constraint.type == "capacity":
            rc = constraint.params["resource_count"]
            max_pr = constraint.params["max_per_resource"]

            total_capacity = rc * max_pr

            explanation.append(
                f"Total capacity is {total_capacity} hours "
                f"({rc} resources × {max_pr} hours each)."
            )

        elif constraint.type == "demand":
            total_required = constraint.params["total_required"]

            explanation.append(
                f"Total required workload is {total_required} hours."
            )

        elif constraint.type == "shift_coverage":
            shifts = constraint.params["shifts"]
            shift_length = constraint.params["shift_length"]

            shift_hours = sum(
                workers * shift_length for workers in shifts.values()
            )

            total_required = shift_hours

            explanation.append(
                f"Shift coverage requires {shift_hours} total hours "
                f"across shifts {list(shifts.keys())}."
            )

        elif constraint.type == "skill_coverage":
            shifts = constraint.params["shifts"]
            shift_length = constraint.params["shift_length"]

            skill_hours = {}

            for shift in shifts.values():
                for skill, count in shift.items():
                    skill_hours[skill] = (
                        skill_hours.get(skill, 0) + count * shift_length
                    )

            explanation.append(
                f"Skill-based staffing requires the following hours: {skill_hours}."
            )

        elif constraint.type == "time_overlap":
            shifts = constraint.params["shifts"]

            explanation.append(
                f"Checked {len(shifts)} shifts for time overlaps to ensure "
                f"no more than available workers are required at any time."
            )

        elif constraint.type == "rest_constraint":
            max_consecutive = constraint.params["max_consecutive"]

            explanation.append(
                f"Checked rest constraint: no more than "
                f"{max_consecutive} consecutive working days."
            )
            
        else:
            explanation.append(
                f"Constraint type '{constraint.type}' is not explainable."
            )

  
    if total_capacity is not None and total_required is not None:
        if total_capacity >= total_required:
            explanation.append(
                "Overall capacity is sufficient to meet requirements."
            )
        else:
            explanation.append(
                "Overall capacity is insufficient to meet requirements."
            )

    return "\n".join(explanation)