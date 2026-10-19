"""
Student Performance Analysis System
Reads student marks from a CSV file, applies OOP concepts, and generates a report.
"""

import csv
from abc import ABC, abstractmethod
from pathlib import Path


class Student(ABC):
    """Abstract base class representing a student."""

    def __init__(self, student_id, first_name, last_name, programme, marks):
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._programme = programme
        self.__marks = {}
        self.update_marks(marks)

    # Read-only properties provide controlled access to student information.
    @property
    def student_id(self):
        return self._student_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def programme(self):
        return self._programme

    @property
    def marks(self):
        # Return a copy so callers cannot directly change the private dictionary.
        return self.__marks.copy()

    def update_marks(self, new_marks):
        """Validate and update subject marks."""
        if not new_marks:
            raise ValueError("A student must have at least one subject mark.")
        validated = {}
        for subject, mark in new_marks.items():
            mark = float(mark)
            if not 0 <= mark <= 100:
                raise ValueError(f"{subject} mark must be between 0 and 100.")
            validated[str(subject)] = mark
        self.__marks = validated

    def average_score(self):
        """Calculate the average across all subjects."""
        return sum(self.__marks.values()) / len(self.__marks)

    def grade(self):
        """Assign a grade using a clearly defined grading scale."""
        average = self.average_score()
        if average >= 80:
            return "A"
        if average >= 70:
            return "B"
        if average >= 60:
            return "C"
        if average >= 50:
            return "D"
        return "E"

    @staticmethod
    def calculate_average(*marks):
        """
        Flexible interface: accepts any number of marks, e.g.
        calculate_average(70, 80, 90) or calculate_average(*[70, 80, 90]).
        """
        if not marks:
            raise ValueError("Supply at least one mark.")
        numeric_marks = [float(mark) for mark in marks]
        if any(mark < 0 or mark > 100 for mark in numeric_marks):
            raise ValueError("Every mark must be between 0 and 100.")
        return sum(numeric_marks) / len(numeric_marks)

    @abstractmethod
    def student_type_info(self):
        """Subclasses must provide information about their student type."""
        pass


class AIUStudent(Student):
    """A standard AIU student."""

    def student_type_info(self):
        # Implementation of the abstract method.
        return f"{self.full_name} is an AIU student in {self.programme}."


class ScholarshipStudent(AIUStudent):
    """An AIU student who can qualify for a scholarship."""

    def __init__(self, student_id, first_name, last_name, programme, marks,
                 scholarship_amount=0):
        super().__init__(student_id, first_name, last_name, programme, marks)
        self.scholarship_amount = float(scholarship_amount)

    def is_eligible(self):
        """The assignment defines eligibility as an average of at least 85."""
        return self.average_score() >= 85

    def student_type_info(self):
        # Method overriding: provide scholarship-specific behaviour.
        if self.is_eligible():
            return (f"{self.full_name} is scholarship-eligible "
                    f"(KES {self.scholarship_amount:,.2f}).")
        return f"{self.full_name} is not scholarship-eligible."


class PerformanceAnalyzer:
    """Analyzes a collection of student objects (composition)."""

    def __init__(self, students):
        if not students:
            raise ValueError("At least one student is required for analysis.")
        self.students = students

    def highest_average(self):
        return max(self.students, key=lambda student: student.average_score())

    def lowest_average(self):
        return min(self.students, key=lambda student: student.average_score())

    def class_average(self):
        return sum(student.average_score() for student in self.students) / len(self.students)


def load_students(csv_file):
    """Read the CSV and create the appropriate student objects."""
    students = []
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required_columns = {"StudentID", "FName", "LName", "Programme",
                            "Math", "English", "Science"}
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV is missing one or more required columns.")

        for row in reader:
            marks = {
                "Math": float(row["Math"]),
                "English": float(row["English"]),
                "Science": float(row["Science"]),
            }
            average = sum(marks.values()) / len(marks)
            # Students with an average >= 85 are represented as scholarship students.
            if average >= 85:
                student = ScholarshipStudent(
                    row["StudentID"], row["FName"], row["LName"],
                    row["Programme"], marks, scholarship_amount=20000 
                )
            else:
                student = AIUStudent(
                    row["StudentID"], row["FName"], row["LName"],
                    row["Programme"], marks
                )
            students.append(student)
    return students


def generate_report(students, analyzer, output_file):
    """Create and save a readable report."""
    lines = [
        "=" * 72,
        "             STUDENT PERFORMANCE ANALYSIS REPORT",
        "=" * 72,
    ]

    for student in students:
        lines.extend([
            "",
            f"Student ID : {student.student_id}",
            f"Name       : {student.full_name}",
            f"Programme  : {student.programme}",
            "Subject marks:",
        ])
        for subject, mark in student.marks.items():
            lines.append(f"  {subject:<10}: {mark:.1f}")
        lines.extend([
            f"Average    : {student.average_score():.2f}%",
            f"Grade      : {student.grade()}",
        ])
        if isinstance(student, ScholarshipStudent):
            status = "Eligible" if student.is_eligible() else "Not eligible"
            lines.append(f"Scholarship: {status} (KES {student.scholarship_amount:,.2f})")
        else:
            lines.append("Scholarship: Not eligible (average below 85%)")
        lines.append(f"Student type: {student.student_type_info()}")

    highest = analyzer.highest_average()
    lowest = analyzer.lowest_average()
    lines.extend([
        "",
        "-" * 72,
        "CLASS SUMMARY",
        "-" * 72,
        f"Highest average : {highest.full_name} ({highest.average_score():.2f}%)",
        f"Lowest average  : {lowest.full_name} ({lowest.average_score():.2f}%)",
        f"Class average   : {analyzer.class_average():.2f}%",
        "",
        "REFLECTION",
        "A challenge was connecting CSV text values to validated numeric marks and",
        "organizing the classes so that each responsibility is handled in one place.",
        "Using small methods, validation, and inheritance made the program easier",
        "to test and maintain.",
        "",
        "AI USE DECLARATION",
        "AI assistance was used to help plan, explain, and review the program.",
        "I reviewed the code and am responsible for understanding, testing, and",
        "explaining the final submission in accordance with my institution's rules.",
        "=" * 72,
    ])
    report_text = "\n".join(lines)
    Path(output_file).write_text(report_text, encoding="utf-8")
    return report_text


def main():
    folder = Path(__file__).resolve().parent
    csv_file = folder / "students.csv"
    report_file = folder / "performance_report.txt"

    students = load_students(csv_file)
    analyzer = PerformanceAnalyzer(students)

    # Polymorphism: the same method call behaves according to each object's type.
    print("POLYMORPHISM DEMONSTRATION")
    for student in students:
        print("-", student.student_type_info())

    # Flexible argument demonstration.
    print("\nFLEXIBLE METHOD DEMONSTRATION")
    print("Average of 70, 80, 90:", f"{Student.calculate_average(70, 80, 90):.2f}")

    report = generate_report(students, analyzer, report_file)
    print("\n" + report)
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()
