from src.schema import Constraint, SchedulingProblem
from src.classifier import classify_problem
from src.verifier import check_feasibility


def test_rest_constraint_feasible():
    capacity = Constraint(
        type="capacity",
        params={"resource_count": 10, "max_per_resource": 8}
    )

    rest = Constraint(
        type="rest_constraint",
        params={
            "max_consecutive": 5,
            "schedule": [
                "work", "work", "work", "work", "work",
                "rest", "work"
            ]
        }
    )

    problem = SchedulingProblem(
        constraints=[capacity, rest]
    )

    assert classify_problem(problem) == "SUPPORTED"
    assert check_feasibility(problem) is True