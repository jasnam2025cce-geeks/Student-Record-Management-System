from models.student import Student
from repository.student_repository import StudentRepository
from typing import List, Optional, Tuple

class StudentService:
    def __init__(self):
        self.repo = StudentRepository()

    def add_student(self, name: str, age: int, gender: str, contact: str = "") -> Tuple[bool, str]:
        if not name or age <= 0:
            return False, "Invalid name or age."
        student = Student(name=name, age=age, gender=gender, contact=contact)
        student_id = self.repo.add_student(student)
        return True, f"Student added successfully with ID {student_id}"

    def get_all_students(self) -> List[Student]:
        return self.repo.get_all_students()

    def get_student(self, student_id: int) -> Optional[Student]:
        return self.repo.get_student(student_id)

    def delete_student(self, student_id: int) -> Tuple[bool, str]:
        if self.repo.delete_student(student_id):
            return True, f"Student {student_id} deleted successfully."
        return False, f"Student {student_id} not found."
