from repository.grade_repository import GradeRepository
from repository.student_repository import StudentRepository
from typing import Dict, Any, List
from collections import defaultdict

class AnalyticsService:
    def __init__(self):
        self.grade_repo = GradeRepository()
        self.student_repo = StudentRepository()

    def calculate_student_gpa(self, student_id: int) -> float:
        grades = self.grade_repo.get_grades_by_student(student_id)
        if not grades:
            return 0.0
        total_score = sum(g.score for g in grades)
        return round(total_score / len(grades), 2)

    def get_student_performance(self, student_id: int) -> Dict[str, Any]:
        grades = self.grade_repo.get_grades_by_student(student_id)
        if not grades:
            return {"average": 0.0, "grades": {}}
        
        grades_dict = {g.subject: g.score for g in grades}
        avg = sum(grades_dict.values()) / len(grades)
        return {"average": round(avg, 2), "grades": grades_dict}

    def get_class_averages(self) -> Dict[str, float]:
        grades = self.grade_repo.get_all_grades()
        if not grades:
            return {}
        
        subject_totals = defaultdict(float)
        subject_counts = defaultdict(int)
        for g in grades:
            subject_totals[g.subject] += g.score
            subject_counts[g.subject] += 1
            
        return {subject: round(total / subject_counts[subject], 2) 
                for subject, total in subject_totals.items()}

    def get_top_performers(self, top_n: int = 3) -> List[Dict[str, Any]]:
        students = self.student_repo.get_all_students()
        grades = self.grade_repo.get_all_grades()
        
        if not students or not grades:
            return []

        student_totals = defaultdict(float)
        student_counts = defaultdict(int)
        for g in grades:
            student_totals[g.student_id] += g.score
            student_counts[g.student_id] += 1
            
        student_averages = {sid: total / student_counts[sid] 
                            for sid, total in student_totals.items()}
        
        student_map = {s.id: s.name for s in students}
        
        results = []
        for sid, avg in student_averages.items():
            if sid in student_map:
                results.append({
                    'student_id': sid,
                    'name': student_map[sid],
                    'average_score': round(avg, 2)
                })
                
        results.sort(key=lambda x: x['average_score'], reverse=True)
        return results[:top_n]
