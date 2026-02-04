from src.schema import Constraint, SchedulingProblem
from src.verifier import check_feasibility
from src.classifier import classify_problem

def test_infeasible_case():
    capacity = Constraint(
        type="capacity",
        params={"resource_count": 8, "max_per_resource": 8}
    )

    demand = Constraint(
        type="demand",
        params={"total_required": 80}
    )

    problem = SchedulingProblem(constraints=[capacity, demand])

    assert classify_problem(problem) == "SUPPORTED"
    assert check_feasibility(problem) is False

def test_feasible_case():
    capacity = Constraint(
        type="capacity",
        params={"resource_count": 8, "max_per_resource": 8}
    )

    demand = Constraint(
        type="demand",
        params={"total_required": 60}
    )

    problem = SchedulingProblem(constraints=[capacity, demand])

    assert classify_problem(problem) == "SUPPORTED"
    assert check_feasibility(problem) is True

def test_out_of_scope_case():
    capacity = Constraint(
        type="capacity",
        params={"resource_count": 8, "max_per_resource": 8}
    )

    weird = Constraint(
        type="time_slot",
        params={"start": 9, "end": 17}
    )

    problem = SchedulingProblem(constraints=[capacity, weird])

    assert classify_problem(problem) == "OUT_OF_SCOPE"
