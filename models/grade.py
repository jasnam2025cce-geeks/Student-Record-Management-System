from dataclasses import dataclass
from typing import Optional

@dataclass
class Grade:
    student_id: int
    subject: str
    score: float
    id: Optional[int] = None
