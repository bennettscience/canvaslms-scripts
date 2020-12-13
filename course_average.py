from canvasapi import Canvas
from config import PROD_KEY, PROD_URL

canvas = Canvas(PROD_URL, PROD_KEY)

course = canvas.get_course(12345)
section = course.get_section(99999, include="students")

# for s in sections if you loop
enrolls = section.get_enrollments(include="total_scores")

grades = []
for e in enrolls:
    grades.append(int(e.grades['final_score']))

calculated = sum(grades) / len(grades)

print(calculated)