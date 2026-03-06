from src.constraint_definitions import CONSTRAINT_DEFINITIONS


def validate_constraints(constraints: list) -> list:
    missing = []
    present_types = {c.type for c in constraints}

    if "skill_coverage" in present_types:
        required_to_skip = {"capacity", "shift_coverage"}
    else:
        required_to_skip = set()

    for constraint_type, definition in CONSTRAINT_DEFINITIONS.items():
        if constraint_type in required_to_skip:
            continue
        if definition["required"] and constraint_type not in present_types:
            missing.append(constraint_type)

    for c in constraints:
        if c.type == "capacity":
            count = c.params.get("resource_count") or c.params.get("total_workers", 0)
            if count == 0 and "capacity" not in missing:
                missing.append("capacity")

    return missing