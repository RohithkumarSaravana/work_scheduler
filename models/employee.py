from dataclasses import dataclass

@dataclass
class Employee:
    employee_id: str
    name: str
    shift: str
    employment_type: str
    start_time: str = None
    end_time: str = None
    available: bool = True