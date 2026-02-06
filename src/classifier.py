from src.schema import SchedulingProblem
SUPPORTED_CONSTRAINTS = {
    "capacity",
    "demand",
    "shift_coverage",
    "skill_coverage",
    "time_overlap",
    "rest_constraint"
}

def classify_problem(problem: SchedulingProblem) -> str:
    
    for constraint in problem.constraints:
        if constraint.type not in SUPPORTED_CONSTRAINTS:
            return "OUT_OF_SCOPE"

    return "SUPPORTED"
