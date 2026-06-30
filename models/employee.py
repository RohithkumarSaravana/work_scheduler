from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    shift: str
    employment_type: str
    start_time: str = None
    end_time: str = None
    available: bool = True