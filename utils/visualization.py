import sys
from typing import Dict, Any

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class PlottingUtil:
    @staticmethod
    def _print_ascii_bar_chart(title: str, data: Dict[str, float]):
        print(f"\n--- {title} ---")
        if not data:
            print("No data available.")
            return
            
        max_val = max(data.values()) if data else 100
        if max_val == 0:
            max_val = 1
            
        for key, value in data.items():
            bar_len = int((value / max_val) * 40)
            bar = '█' * bar_len
            print(f"{key[:12]:<12} | {bar} {value:.2f}")
        print("-" * 50)

    @staticmethod
    def plot_student_performance(student_name: str, grades_dict: Dict[str, float]):
        if not grades_dict:
            print("No grades available to plot.")
            return

        if MATPLOTLIB_AVAILABLE:
            subjects = list(grades_dict.keys())
            scores = list(grades_dict.values())

            plt.figure(figsize=(8, 5))
            plt.bar(subjects, scores, color='skyblue')
            plt.xlabel('Subjects')
            plt.ylabel('Scores')
            plt.title(f'Academic Performance: {student_name}')
            plt.ylim(0, 100)
            
            for i, score in enumerate(scores):
                plt.text(i, score + 1, str(score), ha='center')

            plt.tight_layout()
            plt.show()
        else:
            PlottingUtil._print_ascii_bar_chart(f"Performance: {student_name}", grades_dict)

    @staticmethod
    def plot_class_averages(averages_dict: Dict[str, float]):
        if not averages_dict:
            print("No data available to plot.")
            return

        if MATPLOTLIB_AVAILABLE:
            subjects = list(averages_dict.keys())
            averages = list(averages_dict.values())

            plt.figure(figsize=(8, 5))
            plt.bar(subjects, averages, color='lightgreen')
            plt.xlabel('Subjects')
            plt.ylabel('Average Scores')
            plt.title('Class Average by Subject')
            plt.ylim(0, 100)
            
            for i, avg in enumerate(averages):
                plt.text(i, avg + 1, str(avg), ha='center')

            plt.tight_layout()
            plt.show()
        else:
            PlottingUtil._print_ascii_bar_chart("Class Averages", averages_dict)
