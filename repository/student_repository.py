from models.student import Student
from repository.database_manager import DatabaseManager
from typing import List, Optional

class StudentRepository:
    def __init__(self):
        DatabaseManager.initialize_database()

    def add_student(self, student: Student) -> int:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, gender, contact) VALUES (?, ?, ?, ?)",
            (student.name, student.age, student.gender, student.contact)
        )
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()
        return student_id

    def get_student(self, student_id: int) -> Optional[Student]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Student(id=row['id'], name=row['name'], age=row['age'], gender=row['gender'], contact=row['contact'])
        return None

    def get_all_students(self) -> List[Student]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        return [Student(id=r['id'], name=r['name'], age=r['age'], gender=r['gender'], contact=r['contact']) for r in rows]

    def update_student(self, student: Student) -> bool:
        if not student.id:
            return False
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET name=?, age=?, gender=?, contact=? WHERE id=?",
            (student.name, student.age, student.gender, student.contact, student.id)
        )
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return updated

    def delete_student(self, student_id: int) -> bool:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        deleted = cursor.rowcount > 0
        # Also delete associated grades
        cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()
        return deleted
