from dataclasses import dataclass
from typing import Optional

@dataclass
class Student:
    name: str
    age: int
    gender: str
    contact: Optional[str] = None
    id: Optional[int] = None
