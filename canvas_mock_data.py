from faker import Faker
from canvasapi import Canvas

from config import API_URL, API_KEY


canvas = Canvas(API_URL, API_KEY)
fake = Faker()


def generate_users(num_users, account_id):
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


def generate_courses(num_courses, account_id):
    account = canvas.get_account(account_id)

    for i in range(1, num_courses + 1):
        course_dict = {
            'name': fake.catch_phrase().title(),
            'course_code': fake.bothify(text='???-####').upper(),
            'offer': True
        }

        account.create_course(course=course_dict)
