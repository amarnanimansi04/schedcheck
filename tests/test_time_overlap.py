from src.schema import Constraint, SchedulingProblem
from src.classifier import classify_problem
from src.verifier import check_feasibility


def test_time_overlap_feasible():
    capacity = Constraint(
        type="capacity",
        params={"resource_count": 12, "max_per_resource": 8}
    )

    time_overlap = Constraint(
        type="time_overlap",
        params={
            "shifts": [
                {"name": "morning", "start": 8, "end": 16},
                {"name": "evening", "start": 16, "end": 24},
                {"name": "night", "start": 0, "end": 8}
            ],
            "max_workers": {
                "morning": 4,
                "evening": 4,
                "night": 2
            },
            "total_workers": 12
        }
    )

    problem = SchedulingProblem(
        constraints=[capacity, time_overlap]
    )

    assert classify_problem(problem) == "SUPPORTED"
    assert check_feasibility(problem) is True