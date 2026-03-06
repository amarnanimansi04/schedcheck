CONSTRAINT_DEFINITIONS = {
    "capacity": {
        "required": True,
        "clarification": (
            "How many total workers are available?"
        ),
    },
    "shift_coverage": {
        "required": True,
        "clarification": (
            "How many shifts are there and how many workers are required "
            "per shift? Please answer in full sentence format."
        ),
    },
    "skill_coverage": {
        "required": False,
        "clarification": (
            "Are there different skill types (e.g., senior, junior)? "
            "If yes, how many of each are available and required per shift?"
        ),
    },
    "time_overlap": {
        "required": False,
        "clarification": (
            "Do shifts have specific start and end times?"
        ),
    },
    "rest_constraint": {
        "required": False,
        "clarification": (
            "Is there a minimum rest time required between shifts?"
        ),
    },
}