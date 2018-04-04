from __future__ import print_function, unicode_literals

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


def generate_quizzes(course_id, min_quizzes=1, max_quizzes=5):
    """
    Create randomized quizzes in a course.

    :param course_id: The Canvas Course to create quizzes in.
    :type course_id: int
    :param min_quizzes: The minimum number of quizzes to create.
    :type min_quizzes: int
    :param max_quizzes: The maximum number of quizzes to create.
    :type max_quizzes: int
    """
    course = canvas.get_course(course_id)
    num_quizzes = fake.random_int(min_quizzes, max_quizzes)

    QUIZ_TYPES = ['practice_quiz', 'assignment', 'graded_survey', 'survey']

    for i in range(num_quizzes):
        course.create_quiz(quiz={
            'title': fake.bs().title(),
            'description': fake.text(max_nb_chars=fake.random_int(100, 500)),
            'quiz_type': fake.random_element(QUIZ_TYPES),
            'time_limit': fake.random_int(1, 30) * 5 if fake.boolean(50) else None,
            'published': fake.boolean(75),
            'allowed_attempts': fake.random_int(1, 3) if fake.boolean(75) else -1
        })

    # TODO: add quiz questions


def generate_assignments(course_id, min_assignments=5, max_assignments=10):
    """
    Create randomized assignments in a course.

    :param course_id: The Canvas Course to create assignments in.
    :type course_id: int
    :param min_assignments: The minimum number of assignments to create.
    :type min_assignments: int
    :param max_assignments: The maximum number of assignments to create.
    :type max_assignments: int
    """
    def get_sub_types():
        """
        Return a list of valid sub types.

        :rtype: list
        """
        ASSIGN_SUB_TYPES = {
            'online': ['online_upload', 'online_text_entry', 'online_url'],
            'offline': ['online_quiz', 'none', 'on_paper', 'discussion_topic', 'external_tool']
        }

        if fake.boolean(25):  # 25% chance of being offline only
            # if not online, allow only one type of submission from the offline group
            return [fake.random_element(ASSIGN_SUB_TYPES['offline'])]

        # if online, pick at least one online (and possibly some offline) sub types
        online = fake.random_sample(ASSIGN_SUB_TYPES['online'], fake.random_int(1, 3))
        offline = fake.random_sample(ASSIGN_SUB_TYPES['offline'], fake.random_int(0, 3))
        return list(online | offline)

    course = canvas.get_course(course_id)

    num_assignments = fake.random_int(min_assignments, max_assignments)

    for i in range(num_assignments):
        submission_types = get_sub_types()
        course.create_assignment(assignment={
            'name': fake.bs().title(),
            'submission_types': submission_types,
            'description': fake.text(max_nb_chars=fake.random_int(100, 500)),
            'published': fake.boolean(75)
        })
