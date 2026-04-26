from models.grade import Grade
from repository.database_manager import DatabaseManager
from typing import List

class GradeRepository:
    def __init__(self):
        DatabaseManager.initialize_database()
        
    def add_grade(self, grade: Grade) -> int:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO grades (student_id, subject, score) VALUES (?, ?, ?)",
            (grade.student_id, grade.subject, grade.score)
        )
        conn.commit()
        grade_id = cursor.lastrowid
        conn.close()
        return grade_id

    def get_grades_by_student(self, student_id: int) -> List[Grade]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grades WHERE student_id = ?", (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Grade(id=r['id'], student_id=r['student_id'], subject=r['subject'], score=r['score']) for r in rows]

    def get_all_grades(self) -> List[Grade]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grades")
        rows = cursor.fetchall()
        conn.close()
        return [Grade(id=r['id'], student_id=r['student_id'], subject=r['subject'], score=r['score']) for r in rows]

    def delete_grade(self, grade_id: int) -> bool:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
