from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Constraint:
    type: str
    params: Dict[str, int]

@dataclass
class SchedulingProblem:
    constraints: List[Constraint]




