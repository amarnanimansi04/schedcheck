from src.constraint_definitions import CONSTRAINT_DEFINITIONS


def generate_clarification(missing_types: list) -> str:
    questions = []

    for constraint_type in missing_types:
        definition = CONSTRAINT_DEFINITIONS.get(constraint_type)
        if definition:
            questions.append(definition["clarification"])

    return "\n".join(questions)