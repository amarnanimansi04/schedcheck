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


def build_problem(parsed_json):
    constraints = []
    for c in parsed_json.get("constraints", []):
        constraints.append(
            Constraint(type=c["type"], params=c["params"])
        )
    return SchedulingProblem(constraints=constraints)


def run_pipeline(user_text):
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

        additional_input = input("\nYour answer: ")

        # Combine original and clarification answer
        combined_text = user_text + "\n" + additional_input

        # Re-run parsing
        parsed = parse_constraints(combined_text)

        if parsed is None:
            print("Still invalid. Stopping execution.")
            return

        problem = build_problem(parsed)

        # Validate again
        missing = validate_constraints(problem.constraints)

        if missing:
            print("Still incomplete after clarification. Stopping execution.")
            return

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

    print("\nFeasible:", feasible)

    if feasible:
        print("\n--- Generated Schedule ---")
        print(schedule)

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
                
    print("\n--- Explanation ---")
    print(explain(problem))


if __name__ == "__main__":
    print("Describe your scheduling problem (press Enter on empty line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    text = " ".join(lines)
    run_pipeline(text)