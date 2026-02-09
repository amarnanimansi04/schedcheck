from ortools.sat.python import cp_model


def generate_basic_schedule(problem):
    capacity = None
    shifts = None

    for c in problem.constraints:
        if c.type == "capacity":
            capacity = c.params["resource_count"]
        if c.type == "shift_coverage":
            shifts = c.params["shifts"]

    if capacity is None or shifts is None:
        return None

    nurses = range(capacity)
    shift_names = list(shifts.keys())

    model = cp_model.CpModel()

    
    assign = {}
    for n in nurses:
        for s in shift_names:
            assign[(n, s)] = model.NewBoolVar(f"n{n}_s{s}")

    
    for s in shift_names:
        model.Add(sum(assign[(n, s)] for n in nurses) == shifts[s])

    
    for n in nurses:
        model.Add(sum(assign[(n, s)] for s in shift_names) <= 1)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        return None

    schedule = {}
    for s in shift_names:
        schedule[s] = [
            f"Nurse{n}"
            for n in nurses
            if solver.Value(assign[(n, s)]) == 1
        ]

    return schedule