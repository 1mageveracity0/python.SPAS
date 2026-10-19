STUDENT PERFORMANCE ANALYSIS SYSTEM
====================================

Files:
- student_performance.py : Python source code
- students.csv           : CSV dataset with five student records
- performance_report.txt: Generated report (created when the Python program runs)

How to run:
1. Keep all three files in the same folder.
2. Open that folder in VS Code.
3. Open Terminal > New Terminal.
4. Run: python student_performance.py

The program uses only Python's standard library; no pip installation is needed.

Design notes:
- Student is an abstract base class.
- AIUStudent implements the abstract student_type_info() method.
- ScholarshipStudent inherits from AIUStudent and overrides student_type_info().
- PerformanceAnalyzer analyzes student objects.
- calculate_average(*marks) accepts a variable number of marks.
- Grade scale used in this example: A >= 80, B >= 70, C >= 60, D >= 50, otherwise E.
- Scholarship eligibility follows the assignment threshold of average >= 85.
- The scholarship amount of KES 20,000 is an example value for demonstration; replace it if your lecturer specifies a different amount.

Before submission:
Read and understand the code, run it yourself, and make sure you can explain the OOP concepts during physical marking. Follow your institution's rules for declaring AI assistance.
