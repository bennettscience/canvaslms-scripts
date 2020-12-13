"""
Duplicate enrollments from one course into another
"""

from canvasapi import Canvas
from config import PROD_KEY, PROD_URL

template_course_id = 12345 # Canvas course ID
new_course_id = 99999

canvas = Canvas(PROD_URL, PROD_KEY)

template_course = canvas.get_course(template_course_id)
new_course = canvas.get_course(new_course_id)

# Open the template course section by section and get any sections
# already in the new course.
template_sections = template_course.get_sections()
new_sections = [section.name for section in new_course.get_sections()]

# A big loop to get everyone in each section
for section in template_sections:
    # If the section you're checking is NOT in the new course, do this
    if not section.name in new_sections:
        print(f'Creating section {section.name}')
        # Get all enrolled users in the section.
        enrollments = section.get_enrollments()
        # Add it to the list so you don't do this twice. Not sure this is necessary...
        new_sections.append(section.name)
        course_section = {
            "name": section.name,
        }
        # make the section in Canvas
        new_section = new_course.create_course_section(course_section=course_section)
        
        # Only for updating the console
        count = 0
        for e in enrollments:
            student = e.user['id']
            print(f'Enrolling {e.user["name"]}')
            count += 1
            # Set their enrollment to active so they don't have to accept a course invite.
            enrollment = {
                "course_section_id": new_section.id,
                "notify": False,
                "enrollment_state": "active"
            }
            try:
                new_course.enroll_user(student, "StudentEnrollment", enrollment=enrollment)
            except Exception as e:
                print(e)
        print(f'Enrolled {count} users in {new_section.name}')