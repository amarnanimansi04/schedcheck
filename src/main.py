import os
if os.getenv("LLM_PROVIDER") == "mock":
    from src.llm_mock import parse_constraints
else:
    from src.llm_interface import parse_constraints
from src.schema import Constraint, SchedulingProblem
from src.classifier import classify_problem
from src.explainer import explain
from src.solver import generate_basic_schedule
from src.constraint_validator import validate_constraints
from src.clarifier import generate_clarification
from src.explainer import explain_infeasible

def build_problem(parsed_json):
    constraints = []
    for c in parsed_json.get("constraints", []):
        constraints.append(
            Constraint(type=c["type"], params=c["params"])
        )
    return SchedulingProblem(constraints=constraints)


def run_pipeline(user_text):
    result = {
        "feasible": None,
        "schedule": None,
        "conflict": None,
        "explanation": None
    }

    print("\n--- USER INPUT ---")
    print(user_text)

    parsed = parse_constraints(user_text)
    print("\n--- LLM PARSED CONSTRAINTS ---")
    print(parsed)
    if parsed is None:
        print("Stopping execution due to invalid LLM output.")
        return

    problem = build_problem(parsed)

    # --- Constraint Validation ---
    missing = validate_constraints(problem.constraints)

    if missing:
        print("\n⚠️ Missing required scheduling details:")
        for item in missing:
            print(f"- {item}")

        clarification_question = generate_clarification(missing)
        print("\n🤖 Clarification Needed:")
        print(clarification_question)

        # REPLACE WITH:
        return {
            "feasible": False,
            "schedule": None,
            "conflict": f"Missing details: {', '.join(missing)}",
            "explanation": "",
            "needs_clarification": True,
            "clarification_question": clarification_question
        }

    classification = classify_problem(problem)
    print("\nClassification:", classification)

    if classification != "SUPPORTED":
        print("Problem not supported yet.")
        return

    schedule = generate_basic_schedule(problem)

    if schedule is None:
        feasible = False
    else:
        feasible = True

    result["feasible"] = feasible
    print("\nFeasible:", feasible)

    if feasible:
        print("\n--- Generated Schedule ---")
        print(schedule)

        result["schedule"] = schedule
    
        if schedule:
            assigned = set(n for workers in schedule.values() for n in workers)

            total = 0
            for c in problem.constraints:
                if c.type == "capacity":
                    total += c.params["resource_count"]
                elif c.type == "skill_coverage":
                    total += sum(c.params["available"].values())

            if total > 0:
                utilization = round(100 * len(assigned) / total, 1)

                print("\n--- Assignment Summary ---")
                print(f"Assigned: {len(assigned)} nurses")
                print(f"Unassigned: {total - len(assigned)} nurses")
                print(f"Utilization: {utilization}%")
                result["utilization"] = utilization
                result["assigned_workers"] = len(assigned)
                result["total_workers"] = total
                result["unassigned_workers"] = total - len(assigned)

    else:
        conflict = explain_infeasible(problem)
        print("\n--- Conflict Explanation ---")
        print(conflict)
        result["conflict"] = conflict

    explanation = explain(problem)

    print("\n--- Explanation ---")
    print(explanation)

    result["explanation"] = explanation

    return result


if __name__ == "__main__":
    print("Describe your scheduling problem (press Enter on empty line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    text = " ".join(lines)
    result = run_pipeline(text)
    