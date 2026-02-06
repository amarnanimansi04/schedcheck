from src.schema import Constraint, SchedulingProblem
from src.verifier import check_feasibility
from src.classifier import classify_problem


def test_hospital_basic_feasible():
    capacity = Constraint(
        type="capacity",
        params={"resource_count": 12, "max_per_resource": 8}
    )

    shift_coverage = Constraint(
        type="shift_coverage",
        params={
            "shifts": {
                "morning": 4,
                "evening": 4,
                "night": 2
            },
            "shift_length": 8
        }
    )

    problem = SchedulingProblem(
        constraints=[capacity, shift_coverage]
    )

    assert classify_problem(problem) == "SUPPORTED"
    assert check_feasibility(problem) is True