from src.schema import SchedulingProblem

def explain(problem: SchedulingProblem) -> str:
    capacity = None
    demand = None

    for constraint in problem.constraints:
        if constraint.type == "capacity":
            rc = constraint.params["resource_count"]
            max_pr = constraint.params["max_per_resource"]
            capacity = rc * max_pr

        elif constraint.type == "demand":
            demand = constraint.params["total_required"]

    if capacity is None or demand is None:
        return "Explanation unavailable: missing required constraints."

    if capacity >= demand:
        return (
            f"The problem is feasible.\n"
            f"Available capacity: {capacity}\n"
            f"Required workload: {demand}"
        )
    else:
        shortfall = demand - capacity
        return (
            f"The problem is infeasible.\n"
            f"Available capacity: {capacity}\n"
            f"Required workload: {demand}\n"
            f"Shortfall: {shortfall}"
        )
