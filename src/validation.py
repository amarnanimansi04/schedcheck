from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class CapacityParams(BaseModel):
    resource_count: int
    max_per_resource: int = 1  


class ShiftCoverageParams(BaseModel):
    shifts: Dict[str, int]
    shift_length: int


class SkillCoverageParams(BaseModel):
    shifts: Dict[str, Dict[str, int]]
    shift_length: int
    available: Dict[str, int]


class TimeOverlapShift(BaseModel):
    name: str
    start: int
    end: int


class TimeOverlapParams(BaseModel):
    shifts: List[TimeOverlapShift]
    max_workers: Dict[str, int]
    total_workers: int


class ConstraintModel(BaseModel):
    type: str
    params: dict


class SchedulingProblemModel(BaseModel):
    constraints: List[ConstraintModel]