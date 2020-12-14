from config import PROD_URL, PROD_KEY
from canvasapi import Canvas
import json

canvas = Canvas(PROD_URL, PROD_KEY)
course_id = 12345  # target course ID
assignment_id = 98765  # target assignment

course = canvas.get_course(course_id)
assignment = course.get_assignment(assignment_id)
submissions = assignment.get_submissions()

for sub in submissions:
    data = json.loads(sub.to_json())
    if data["submitted_at"] is not None:
        sub.edit(submission={"posted_grade": 1.0})
