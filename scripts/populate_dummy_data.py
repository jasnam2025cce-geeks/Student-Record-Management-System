import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.student_service import StudentService
from repository.grade_repository import GradeRepository
from models.grade import Grade
from repository.database_manager import DatabaseManager

def populate():
    DatabaseManager.initialize_database()
    print("Populating dummy data...")
    svc = StudentService()
    repo = GradeRepository()
    
    students = [
        ("Alice Smith", 20, "Female", "alice@example.com"),
        ("Bob Johnson", 21, "Male", "bob@example.com"),
        ("Charlie Brown", 19, "Male", "charlie@example.com"),
        ("Diana Prince", 22, "Female", "diana@example.com")
    ]
    
    ids = []
    for s in students:
        _, msg = svc.add_student(*s)
        ids.append(int(msg.split("ID ")[-1]))
    
    print(f"Added {len(ids)} students.")
    
    import random
    subjects = ["Math", "Science", "History", "English"]
    for sid in ids:
        for subj in subjects:
            score = round(random.uniform(60, 100), 2)
            repo.add_grade(Grade(student_id=sid, subject=subj, score=score))
    
    print("Added grades for all subjects.")
    print("Dummy data population complete!")

if __name__ == "__main__":
    populate()
