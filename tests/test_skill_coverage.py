from src.schema import Constraint, SchedulingProblem
from src.verifier import check_feasibility
from src.classifier import classify_problem


def test_skill_coverage_feasible():
    capacity = Constraint(
        type="capacity",
        params={"resource_count": 12, "max_per_resource": 8}
    )

    skill_coverage = Constraint(
        type="skill_coverage",
        params={
            "shifts": {
                "morning": {"senior": 1, "junior": 2},
                "evening": {"senior": 1, "junior": 2},
                "night": {"senior": 1, "junior": 2}
            },
            "shift_length": 8,
            "available": {
                "senior": 4,
                "junior": 8
            }
        }
    )

    problem = SchedulingProblem(
        constraints=[capacity, skill_coverage]
    )

    assert classify_problem(problem) == "SUPPORTED"
    assert check_feasibility(problem) is True