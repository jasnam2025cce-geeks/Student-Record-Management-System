from services.student_service import StudentService
from services.analytics_service import AnalyticsService
from repository.grade_repository import GradeRepository
from models.grade import Grade
from utils.visualization import PlottingUtil
import sys

class CLI:
    def __init__(self):
        self.student_service = StudentService()
        self.analytics_service = AnalyticsService()
        self.grade_repo = GradeRepository()

    def _print_table(self, headers, rows):
        if not rows:
            print("No data available.")
            return
            
        col_widths = [len(str(h1
                            )) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
                
        fmt_str = " | ".join([f"{{:<{w}}}" for w in col_widths])
        separator = "-+-".join(["-" * w for w in col_widths])
        
        print(fmt_str.format(*headers))
        print(separator)
        for row in rows:
            print(fmt_str.format(*[str(cell) for cell in row]))

    def display_menu(self):
        print("\n" + "="*40)
        print("  STUDENT RECORD MANAGEMENT SYSTEM  ")
        print("="*40)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Add Grades for Student")
        print("4. View Student Performance & Analytics")
        print("5. View Class Analytics (Top Performers & Averages)")
        print("6. Delete Student")
        print("7. Exit")
        print("="*40)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.add_grades()
            elif choice == '4':
                self.view_student_performance()
            elif choice == '5':
                self.view_class_analytics()
            elif choice == '6':
                self.delete_student()
            elif choice == '7':
                print("Exiting System. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def add_student(self):
        print("\n--- Add New Student ---")
        name = input("Name: ")
        try:
            age = int(input("Age: "))
        except ValueError:
            print("Invalid age. Must be a number.")
            return
        gender = input("Gender: ")
        contact = input("Contact: ")
        
        success, msg = self.student_service.add_student(name, age, gender, contact)
        print(msg)

    def view_all_students(self):
        print("\n--- All Students ---")
        students = self.student_service.get_all_students()
        if not students:
            print("No students found.")
            return
        
        table = [[s.id, s.name, s.age, s.gender, s.contact] for s in students]
        self._print_table(["ID", "Name", "Age", "Gender", "Contact"], table)

    def add_grades(self):
        print("\n--- Add Grades ---")
        try:
            student_id = int(input("Enter Student ID: "))
        except ValueError:
            print("Invalid Student ID.")
            return
            
        student = self.student_service.get_student(student_id)
        if not student:
            print("Student not found.")
            return
            
        subject = input("Enter Subject: ")
        try:
            score = float(input("Enter Score (0-100): "))
        except ValueError:
            print("Invalid score. Must be a number.")
            return
            
        grade = Grade(student_id=student_id, subject=subject, score=score)
        self.grade_repo.add_grade(grade)
        print("Grade added successfully!")

    def view_student_performance(self):
        print("\n--- Student Performance ---")
        try:
            student_id = int(input("Enter Student ID: "))
        except ValueError:
            print("Invalid Student ID.")
            return
            
        student = self.student_service.get_student(student_id)
        if not student:
            print("Student not found.")
            return
            
        perf = self.analytics_service.get_student_performance(student_id)
        if not perf["grades"]:
            print("No grades found for this student.")
            return
            
        print(f"\nPerformance for [{student.name}]:")
        table = [[subj, score] for subj, score in perf["grades"].items()]
        self._print_table(["Subject", "Score"], table)
        print(f"Overall GPA / Average: {perf['average']}")
        
        plot_choice = input("Do you want to visualize this performance? (y/n): ").lower()
        if plot_choice == 'y':
            PlottingUtil.plot_student_performance(student.name, perf["grades"])

    def view_class_analytics(self):
        print("\n--- Class Analytics ---")
        averages = self.analytics_service.get_class_averages()
        if not averages:
            print("No grade data available.")
            return
            
        print("\nClass Averages by Subject:")
        table = [[subj, avg] for subj, avg in averages.items()]
        self._print_table(["Subject", "Average Score"], table)
        
        top_performers = self.analytics_service.get_top_performers(3)
        print("\nTop Performers:")
        if top_performers:
            top_table = [[p['student_id'], p['name'], p['average_score']] for p in top_performers]
            self._print_table(["Student ID", "Name", "Average Score"], top_table)
            
        plot_choice = input("Do you want to visualize class averages? (y/n): ").lower()
        if plot_choice == 'y':
            PlottingUtil.plot_class_averages(averages)

    def delete_student(self):
        print("\n--- Delete Student ---")
        try:
            student_id = int(input("Enter Student ID to delete: "))
        except ValueError:
            print("Invalid Student ID.")
            return
            
        success, msg = self.student_service.delete_student(student_id)
        print(msg)
