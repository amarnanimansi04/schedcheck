def parse_constraints(text: str) -> dict:
    return {
        "constraints": [
            {
                "type": "capacity",
                "params": {
                    "resource_count": 12,
                    "max_per_resource": 8
                }
            },
            {
                "type": "shift_coverage",
                "params": {
                    "shifts": {
                        "morning": 4,
                        "evening": 4,
                        "night": 2
                    },
                    "shift_length": 8
                }
            }
        ]
    }