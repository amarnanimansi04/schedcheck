from src.llm_interface import parse_constraints
from src.schema import Constraint, SchedulingProblem
from src.classifier import classify_problem
from src.verifier import check_feasibility
from src.explainer import explain
from src.solver import generate_basic_schedule


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

    problem = build_problem(parsed)

    classification = classify_problem(problem)
    print("\nClassification:", classification)

    if classification != "SUPPORTED":
        print("Problem not supported yet.")
        return

    feasible = check_feasibility(problem)
    print("\nFeasible:", feasible)

    if feasible:
        schedule = generate_basic_schedule(problem)
        print("\n--- Generated Schedule ---")
        print(schedule)

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