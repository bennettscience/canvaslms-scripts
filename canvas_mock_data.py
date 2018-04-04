from faker import Faker
from canvasapi import Canvas

from config import API_URL, API_KEY


canvas = Canvas(API_URL, API_KEY)
fake = Faker()


def generate_users(account_id, num_users):
    """
    Create realistic-looking mock users.

    :param account_id: The Canvas Account to create users in.
    :type account_id: int
    :param num_users: The number of users to create.
    :type num_users: int
    """
    account = canvas.get_account(account_id)

    for i in range(1, num_users + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()

        user = {
            'name': '{} {}'.format(first_name, last_name),
            'short_name': first_name,
            'sortable_name': '{}, {}'.format(last_name, first_name)
        }
        pseudonym = {
            'unique_id': '{}.{}{}@example.com'.format(first_name[0], last_name, i),
            'password': 'password'
        }

        account.create_user(pseudonym, user=user)


def generate_courses(account_id, num_courses):
    """
    Create realistic-looking mock courses.

    :param account_id: The Canvas Account to create courses in.
    :type account_id: int
    :param num_courses: The number of courses to create.
    :type num_courses: int
    """
    account = canvas.get_account(account_id)

    for i in range(1, num_courses + 1):
        course_dict = {
            'name': fake.catch_phrase().title(),
            'course_code': fake.bothify(text='???-####').upper(),
            'offer': True
        }

        account.create_course(course=course_dict)


def generate_enrollments(account_id, min_students=1, max_students=5):
    """
    Enroll random users into each course.

    :param account_id: The Canvas Account to create enrollments in.
    :type account_id: int
    :param min_students: The minimum number of student enrollments to add per course.
    :type min_students: int
    :param max_students: The maximum number of student enrollments to add per course.
    :type max_students: int
    """
    account = canvas.get_account(account_id)

    user_list = [user for user in account.get_users()]
    courses = account.get_courses()

    already_enrolled = []

    for course in courses:
        num_students = fake.random_int(min=min_students, max=max_students)
        for i in range(0, num_students):
            enroll_user = fake.random_element(user_list)

            if enroll_user.id in already_enrolled:
                continue

            enroll_type = 'StudentEnrollment'
            enrollment = {
                'notify': False,
                'enrollment_state': 'active'
            }

            course.enroll_user(enroll_user, enroll_type, enrollment=enrollment)
            already_enrolled.append(enroll_user.id)

        # TODO: Add support for enrolling Teachers/ TAs
