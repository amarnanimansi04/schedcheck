from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Constraint:
    type: str
    params: Dict[str, Any]

@dataclass
class SchedulingProblem:
    constraints: List[Constraint]




