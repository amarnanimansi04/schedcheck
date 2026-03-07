from ortools.sat.python import cp_model
from src.constraint_handlers import HANDLER_REGISTRY


def generate_basic_schedule(problem):
    model = cp_model.CpModel()

    # --- First pass: create empty context ---
    context = {
        "model": model,
        "assign": None,
        "nurses": None,
        "shift_names": None,
        "capacity_total": 0,
    }

    # --- First pass: process non-model constraints (like capacity) ---
    for c in problem.constraints:
        handler = HANDLER_REGISTRY.get(c.type)
        if handler and c.type == "capacity":
            handler(context, c)

    # --- Determine shifts ---
    shift_names = None
    for c in problem.constraints:
        if c.type == "skill_coverage":
            shift_names = list(c.params["shifts"].keys())
            break
        if c.type == "shift_coverage":
            shift_names = list(c.params["shifts"].keys())

    if not shift_names:
        print("❌ Solver stopped: no shifts defined.")
        return None

    context["shift_names"] = shift_names

    # --- Create nurses ---
    nurses = []
    nurse_id = 0

    # Skill case
    skill_constraint = next(
        (c for c in problem.constraints if c.type == "skill_coverage"),
        None
    )

    if skill_constraint:
        available = skill_constraint.params.get("available", {})
        for skill, count in available.items():
            for _ in range(count):
                nurses.append({"id": nurse_id, "skill": skill})
                nurse_id += 1
    else:
        if context["capacity_total"] == 0:
            print("❌ Solver stopped: no workers defined (capacity_total = 0).")
            return None
        for n in range(context["capacity_total"]):
            nurses.append({"id": n, "skill": None})

    context["nurses"] = nurses

    # --- Create assignment variables ---
    assign = {}
    for nurse in nurses:
        for shift in shift_names:
            assign[(nurse["id"], shift)] = model.NewBoolVar(
                f"n{nurse['id']}_s{shift}"
            )

    context["assign"] = assign

    # --- Second pass: apply model constraints ---
    for c in problem.constraints:
        handler = HANDLER_REGISTRY.get(c.type)
        if handler and c.type != "capacity":
            handler(context, c)

    # --- Each nurse works at most 1 shift ---
    for nurse in nurses:
        model.Add(
            sum(assign[(nurse["id"], shift)] for shift in shift_names)
            <= 1
        )

    # --- Objective (stable deterministic output) ---
    model.Minimize(
        sum(
            nurse["id"] * assign[(nurse["id"], shift)]
            for nurse in nurses
            for shift in shift_names
        )
    )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    schedule = {}
    for shift in shift_names:
        schedule[shift] = [
            f"Nurse{nurse['id']}"
            for nurse in nurses
            if solver.Value(assign[(nurse["id"], shift)]) == 1
        ]

    return schedule