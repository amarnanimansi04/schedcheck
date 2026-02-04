from src.schema import Constraint, SchedulingProblem

def check_feasibility(problem: SchedulingProblem) -> bool:
    capacity = None
    demand = None

    for constraint in problem.constraints:
        if constraint.type == "capacity":
            rc = constraint.params["resource_count"]
            max_pr = constraint.params["max_per_resource"]
            capacity = rc * max_pr

        elif constraint.type == "demand":
            demand = constraint.params["total_required"]

        else:
            raise ValueError(f"Unsupported constraint type: {constraint.type}")

    if capacity is None or demand is None:
        raise ValueError("Missing required constraints")

    return capacity >= demand
