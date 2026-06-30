from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    shift: str
    employment_type: str
    available: bool = True