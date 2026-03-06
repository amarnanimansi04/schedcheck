from src.schema import SchedulingProblem


def check_feasibility(problem: SchedulingProblem) -> bool:
    total_capacity = None
    total_required = None
    max_per_resource = None

    for constraint in problem.constraints:

        if constraint.type == "capacity":
            rc = constraint.params["resource_count"]
            max_per_resource = constraint.params["max_per_resource"]
            total_capacity = rc * max_per_resource

        elif constraint.type == "demand":
            total_required = constraint.params["total_required"]

        elif constraint.type == "shift_coverage":
            shifts = constraint.params["shifts"]
            shift_length = constraint.params["shift_length"]

            total_required = sum(
                workers * shift_length
                for workers in shifts.values()
            )

        elif constraint.type == "skill_coverage":
            shifts = constraint.params["shifts"]
            shift_length = constraint.params["shift_length"]
            available = constraint.params["available"]

            required_hours = {}

            for shift in shifts.values():
                for skill, count in shift.items():
                    required_hours[skill] = (
                        required_hours.get(skill, 0) + count * shift_length
                    )

            total_required = sum(required_hours.values())

            for skill, workers in available.items():
                max_hours = workers * shift_length
                if required_hours.get(skill, 0) > max_hours:
                    return False
                
            return True

        elif constraint.type == "time_overlap":
            shifts = constraint.params["shifts"]
            max_workers = constraint.params["max_workers"]
            total_workers = constraint.params["total_workers"]

            # Validate shift time ranges
            for shift in shifts:
                if shift["start"] == shift["end"]:
                    return False

            # Build timeline events
            events = []
            for shift in shifts:
                start = shift["start"]
                end = shift["end"]
                workers = max_workers.get(shift["name"], 0)

                events.append((start, workers))
                events.append((end, -workers))

            # Sweep-line algorithm to detect over-demand
            current_workers = 0
            for _, delta in sorted(events):
                current_workers += delta
                if current_workers > total_workers:
                    return False
        
        elif constraint.type == "rest_constraint":
            max_consecutive = constraint.params["max_consecutive"]
            schedule = constraint.params["schedule"]

            consecutive = 0
            for day in schedule:
                if day == "work":
                    consecutive += 1
                    if consecutive > max_consecutive:
                        return False
                else:
                    consecutive = 0

        else:
            raise ValueError(f"Unsupported constraint type: {constraint.type}")

    if total_required is not None:
        if total_capacity is None:
            return False
        return total_capacity >= total_required

   
    return True