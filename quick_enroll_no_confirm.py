from config import PROD_URL, PROD_KEY
from canvasapi import Canvas

canvas = Canvas(PROD_URL, PROD_KEY)

course = canvas.get_course(12345)
# specify sections if you want to
# wrap the enrollment object in a loop for eac section
# sections = [59592, 59600, 59611]

enrollment = {
    "notify": False,
    "enrollment_state": "active",
}

course.enroll_user(000000, "TeacherEnrollment", enrollment=enrollment)
