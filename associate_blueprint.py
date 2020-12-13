"""
Associate a blueprint course with courses in a subaccount. This does not
sync materials, just adds courses to the blueprint.
"""
import csv
from canvasapi import Canvas
from config import TEST_KEY, TEST_URL, PROD_KEY, PROD_URL

canvas = Canvas(PROD_URL, PROD_KEY)
blueprint_id = 47523
course_ids = []

# Get the blueprint course
blueprint_course = canvas.get_course(blueprint_id).get_blueprint()

# Read a CSV and loop each course ID
with open('file.csv', 'r') as input:
    # Uncomment to skip a header row
    # next(input)
    for row in csv.reader(input):
        # Canvas-formatted CSVs have the course ID is column 1. Change this 
        # reference if you're using a different format.
        course_ids.append(row[0])

# Make a batch association
blueprint_course.update_associated_courses(course_ids_to_add=course_ids)

updated_list = blueprint_course.get_associated_courses()
print(f'{len(list(updated_list))} now associated')

